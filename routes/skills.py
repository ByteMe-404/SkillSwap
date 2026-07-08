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

