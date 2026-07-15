from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.category import Category
from models.user import User
from models.skill import Skill
from models.request import Request

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.home'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html',
        total_users=User.query.count(),
        total_skills=Skill.query.count(),
        total_requests=Request.query.count(),
        total_cats=Category.query.count(),
        recent_users=User.query.order_by(User.created_at.desc()).limit(10).all()
    )

@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    return render_template('admin/categories.html', categories=Category.query.order_by(Category.name).all())

@admin_bp.route('/categories/add', methods=['POST'])
@login_required
@admin_required
def add_category():
    name = request.form.get('name', '').strip()
    icon = request.form.get('icon', 'ti-star').strip()
    if not name:
        flash('Name required.', 'danger')
    elif Category.query.filter_by(name=name).first():
        flash('Category already exists.', 'warning')
    else:
        db.session.add(Category(name=name, icon=icon))
        db.session.commit()
        flash('Category added.', 'success')
    return redirect(url_for('admin.categories'))

@admin_bp.route('/categories/<int:cat_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(cat_id):
    db.session.delete(Category.query.get_or_404(cat_id))
    db.session.commit()
    flash('Deleted.', 'info')
    return redirect(url_for('admin.categories'))

@admin_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    flash(f"User {'activated' if user.is_active else 'deactivated'}.", 'info')
    return redirect(url_for('admin.dashboard'))
