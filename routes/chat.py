from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.chat import Chat
from models.message import Message

chat_bp = Blueprint('chat', __name__)

def _user_chats():
    return Chat.query.filter(
        (Chat.user1_id == current_user.id) | (Chat.user2_id == current_user.id)
    ).order_by(Chat.created_at.desc()).all()

@chat_bp.route('/chats')
@login_required
def index():
    chats = _user_chats()
    return render_template('chat/index.html', chats=chats, active_chat=None, messages=[])

@chat_bp.route('/chats/<int:chat_id>', methods=['GET', 'POST'])
@login_required
def conversation(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.user1_id != current_user.id and chat.user2_id != current_user.id:
        flash('Not authorized.', 'danger')
        return redirect(url_for('chat.index'))

    # AJAX send
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        body = request.form.get('body', '').strip()
        if not body:
            return jsonify(ok=False, error='Empty message'), 400
        msg = Message(chat_id=chat_id, sender_id=current_user.id, body=body)
        db.session.add(msg)
        db.session.commit()
        return jsonify(ok=True, message={
            'id':         msg.id,
            'sender_id':  msg.sender_id,
            'body':       msg.body,
            'created_at': msg.created_at.strftime('%Y-%m-%dT%H:%M:%S')
        })

    # Normal POST (fallback, no JS)
    if request.method == 'POST':
        body = request.form.get('body', '').strip()
        if body:
            db.session.add(Message(chat_id=chat_id, sender_id=current_user.id, body=body))
            db.session.commit()
        return redirect(url_for('chat.conversation', chat_id=chat_id))

    # Mark incoming messages as read
    Message.query.filter_by(chat_id=chat_id, is_read=False).filter(
        Message.sender_id != current_user.id
    ).update({'is_read': True})
    db.session.commit()

    chats    = _user_chats()
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.created_at.asc()).all()
    return render_template('chat/index.html', chats=chats, active_chat=chat, messages=messages)

@chat_bp.route('/chats/<int:chat_id>/poll')
@login_required
def poll(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.user1_id != current_user.id and chat.user2_id != current_user.id:
        return jsonify(messages=[])

    after = request.args.get('after', 0, type=int)
    new_msgs = Message.query.filter(
        Message.chat_id == chat_id,
        Message.id > after
    ).order_by(Message.created_at.asc()).all()

    # Mark polled messages from the other person as read
    for m in new_msgs:
        if m.sender_id != current_user.id and not m.is_read:
            m.is_read = True
    db.session.commit()

    return jsonify(messages=[{
        'id':         m.id,
        'sender_id':  m.sender_id,
        'body':       m.body,
        'created_at': m.created_at.strftime('%Y-%m-%dT%H:%M:%S')
    } for m in new_msgs])
