from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.request import Request
from models.skill import Skill
from models.chat import Chat

requests_bp = Blueprint('requests', __name__)

@requests_bp.route('/requests/send/<int:skill_id>', methods=['POST'])
@login_required
def send(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if skill.user_id == current_user.id:
        flash("You can't request your own skill.", 'warning')
        return redirect(url_for('skills.detail', skill_id=skill_id))
    existing = Request.query.filter_by(skill_id=skill_id, requester_id=current_user.id).first()
    if existing:
        flash('You already sent a request for this skill.', 'warning')
        return redirect(url_for('skills.detail', skill_id=skill_id))
    req = Request(
        skill_id=skill_id, requester_id=current_user.id,
        teacher_id=skill.user_id,
        topic=request.form.get('topic', ''),
        message=request.form.get('message', '').strip()
    )
    db.session.add(req)
    db.session.commit()
    flash('Request sent!', 'success')
    return redirect(url_for('requests.sent'))

@requests_bp.route('/requests/sent')
@login_required
def sent():
    status = request.args.get('status', 'all')
    q = Request.query.filter_by(requester_id=current_user.id)
    if status != 'all':
        q = q.filter_by(status=status)
    reqs = q.order_by(Request.created_at.desc()).all()
    return render_template('requests/sent.html', requests=reqs, status=status)

@requests_bp.route('/requests/received')
@login_required
def received():
    status = request.args.get('status', 'all')
    q = Request.query.filter_by(teacher_id=current_user.id)
    if status != 'all':
        q = q.filter_by(status=status)
    reqs = q.order_by(Request.created_at.desc()).all()
    pending_count = Request.query.filter_by(teacher_id=current_user.id, status='pending').count()
    return render_template('requests/received.html', requests=reqs, status=status, pending_count=pending_count)

@requests_bp.route('/requests/<int:req_id>/accept', methods=['POST'])
@login_required
def accept(req_id):
    req = Request.query.get_or_404(req_id)
    if req.teacher_id != current_user.id:
        flash('Not authorized.', 'danger')
        return redirect(url_for('requests.received'))
    req.status = 'accepted'
    chat = Chat(request_id=req.id, user1_id=req.requester_id, user2_id=req.teacher_id)
    db.session.add(chat)
    db.session.commit()
    flash('Request accepted. Chat opened!', 'success')
    return redirect(url_for('requests.received'))

@requests_bp.route('/requests/<int:req_id>/reject', methods=['POST'])
@login_required
def reject(req_id):
    req = Request.query.get_or_404(req_id)
    if req.teacher_id != current_user.id:
        flash('Not authorized.', 'danger')
        return redirect(url_for('requests.received'))
    req.status = 'rejected'
    db.session.commit()
    flash('Request rejected.', 'info')
    return redirect(url_for('requests.received'))

@requests_bp.route('/requests/<int:req_id>/cancel', methods=['POST'])
@login_required
def cancel(req_id):
    req = Request.query.get_or_404(req_id)
    if req.requester_id != current_user.id:
        flash('Not authorized.', 'danger')
        return redirect(url_for('requests.sent'))
    req.status = 'cancelled'
    db.session.commit()
    flash('Request cancelled.', 'info')
    return redirect(url_for('requests.sent'))
