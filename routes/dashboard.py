from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.skill import Skill
from models.request import Request

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    my_skills     = Skill.query.filter_by(user_id=current_user.id, status='active').count()
    sent_requests = Request.query.filter_by(requester_id=current_user.id).count()
    recv_requests = Request.query.filter_by(teacher_id=current_user.id).count()
    pending_recv  = Request.query.filter_by(teacher_id=current_user.id, status='pending').count()
    recent_sent   = Request.query.filter_by(requester_id=current_user.id).order_by(Request.created_at.desc()).limit(5).all()
    recent_recv   = Request.query.filter_by(teacher_id=current_user.id).order_by(Request.created_at.desc()).limit(5).all()
    return render_template('dashboard/index.html',
        my_skills=my_skills, sent_requests=sent_requests,
        recv_requests=recv_requests, pending_recv=pending_recv,
        recent_sent=recent_sent, recent_recv=recent_recv)
