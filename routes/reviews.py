from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.review import Review
from models.request import Request

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/reviews')
@login_required
def index():
    received = Review.query.filter_by(reviewee_id=current_user.id).order_by(Review.created_at.desc()).all()
    given    = Review.query.filter_by(reviewer_id=current_user.id).order_by(Review.created_at.desc()).all()
    return render_template('reviews/index.html', received=received, given=given)

@reviews_bp.route('/reviews/add/<int:request_id>', methods=['GET', 'POST'])
@login_required
def add(request_id):
    req = Request.query.get_or_404(request_id)
    if req.requester_id != current_user.id or req.status != 'accepted':
        flash('Not authorized.', 'danger')
        return redirect(url_for('reviews.index'))
    if Review.query.filter_by(request_id=request_id, reviewer_id=current_user.id).first():
        flash('Already reviewed.', 'warning')
        return redirect(url_for('reviews.index'))
    if request.method == 'POST':
        db.session.add(Review(
            request_id=request_id, reviewer_id=current_user.id,
            reviewee_id=req.teacher_id,
            rating=int(request.form['rating']),
            comment=request.form.get('comment', '').strip()
        ))
        db.session.commit()
        flash('Review submitted!', 'success')
        return redirect(url_for('reviews.index'))
    return render_template('reviews/add.html', req=req)

@reviews_bp.route('/reviews/<int:review_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(review_id):
    review = Review.query.get_or_404(review_id)
    if review.reviewer_id != current_user.id:
        flash('Not authorized.', 'danger')
        return redirect(url_for('reviews.index'))
    if request.method == 'POST':
        review.rating  = int(request.form['rating'])
        review.comment = request.form.get('comment', '').strip()
        db.session.commit()
        flash('Review updated.', 'success')
        return redirect(url_for('reviews.index'))
    return render_template('reviews/edit.html', review=review)

@reviews_bp.route('/reviews/<int:review_id>/delete', methods=['POST'])
@login_required
def delete(review_id):
    review = Review.query.get_or_404(review_id)
    if review.reviewer_id != current_user.id:
        flash('Not authorized.', 'danger')
        return redirect(url_for('reviews.index'))
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted.', 'info')
    return redirect(url_for('reviews.index'))
