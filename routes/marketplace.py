from flask import Blueprint, render_template, request
from models.skill import Skill
from models.category import Category

marketplace_bp = Blueprint('marketplace', __name__)

@marketplace_bp.route('/marketplace')
def index():
    q           = request.args.get('q', '')
    category_id = request.args.get('category_id', '')
    level       = request.args.get('level', '')
    sort        = request.args.get('sort', 'newest')
    page        = request.args.get('page', 1, type=int)

    sq = Skill.query.filter_by(status='active')
    if q:
        sq = sq.filter(Skill.title.ilike(f'%{q}%') | Skill.short_desc.ilike(f'%{q}%'))
    if category_id:
        sq = sq.filter_by(category_id=int(category_id))
    if level:
        sq = sq.filter_by(level=level)
    sq = sq.order_by(Skill.created_at.asc() if sort == 'oldest' else Skill.created_at.desc())

    skills     = sq.paginate(page=page, per_page=12, error_out=False)
    categories = Category.query.order_by(Category.name).all()
    return render_template('marketplace/index.html',
        skills=skills, categories=categories,
        query=q, selected_category=category_id, selected_level=level, sort=sort)
