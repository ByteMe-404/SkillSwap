import json
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.skill import Skill
from models.category import Category
from models.review import Review
from models.request import Request as SkillRequest

skills_bp = Blueprint('skills', __name__)

@skills_bp.route('/skills')
@login_required
def my_skills():
    skills = Skill.query.filter_by(user_id=current_user.id).order_by(Skill.created_at.desc()).all()
    categories = Category.query.order_by(Category.name).all()
    return render_template('skills/my_skills.html', skills=skills, categories=categories)

@skills_bp.route('/skills/<int:skill_id>')
def detail(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    reviews = Review.query.join(SkillRequest).filter(SkillRequest.skill_id == skill_id).order_by(Review.created_at.desc()).all()
    user_req = None
    if current_user.is_authenticated:
        user_req = SkillRequest.query.filter_by(skill_id=skill_id, requester_id=current_user.id).first()
    return render_template('skills/detail.html', skill=skill, reviews=reviews, user_request=user_req)

@skills_bp.route('/skills/add', methods=['GET', 'POST'])
@login_required
def add():
    categories = Category.query.order_by(Category.name).all()
    if request.method == 'POST':
        skill = Skill(
            user_id=current_user.id,
            category_id=int(request.form['category_id']),
            title=request.form['title'].strip(),
            short_desc=request.form['short_desc'].strip(),
            description=request.form['description'].strip(),
            level=request.form.get('level_sel') or request.form.get('level', 'Beginner'),
            session_duration=request.form.get('session_duration', '45-60 minutes'),
            session_format=request.form.get('session_format', 'Both'),
            max_students=int(request.form.get('max_students', 1)),
            status=request.form.get('status', 'draft')
        )
        raw_topics = request.form.get('topics', '[]')
        try:
            skill.topics = json.loads(raw_topics)
        except Exception:
            skill.topics = []
        skill.outcomes = [o.strip() for o in request.form.getlist('outcomes') if o.strip()]
        skill.availability = request.form.getlist('availability')
        db.session.add(skill)
        db.session.commit()
        flash('Skill added successfully!', 'success')
        return redirect(url_for('skills.my_skills'))
    return render_template('skills/add.html', categories=categories)

@skills_bp.route('/skills/<int:skill_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if skill.user_id != current_user.id:
        flash('Not authorized.', 'danger')
        return redirect(url_for('skills.my_skills'))
    categories = Category.query.order_by(Category.name).all()
    if request.method == 'POST':
        skill.category_id = int(request.form['category_id'])
        skill.title = request.form['title'].strip()
        skill.short_desc = request.form['short_desc'].strip()
        skill.description = request.form['description'].strip()
        skill.level = request.form.get('level', 'Beginner')
        skill.session_duration = request.form.get('session_duration', '45-60 minutes')
        skill.session_format = request.form.get('session_format', 'Both')
        skill.max_students = int(request.form.get('max_students', 1))
        skill.status = request.form.get('status', 'draft')
        raw_topics = request.form.get('topics', '[]')
        try:
            skill.topics = json.loads(raw_topics)
        except Exception:
            skill.topics = []
        skill.outcomes = [o.strip() for o in request.form.getlist('outcomes') if o.strip()]
        skill.availability = request.form.getlist('availability')
        db.session.commit()
        flash('Skill updated.', 'success')
        return redirect(url_for('skills.my_skills'))
    return render_template('skills/edit.html', skill=skill, categories=categories)

@skills_bp.route('/skills/<int:skill_id>/delete', methods=['POST'])
@login_required
def delete(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if skill.user_id != current_user.id:
        flash('Not authorized.', 'danger')
        return redirect(url_for('skills.my_skills'))
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted.', 'info')
    return redirect(url_for('skills.my_skills'))
