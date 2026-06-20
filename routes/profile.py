import os, uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from extensions import db
from models.user import User


profile_bp = Blueprint('profile', __name__)
ALLOWED = {'png', 'jpg', 'jpeg'}



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED


@profile_bp.route('/profile')
@login_required
def view():
    return render_template('profile/view.html', user=current_user)



@profile_bp.route('/profile/edit' , methods=['GET', 'POST'])
@login_required

def edit():
    if request.method == 'POST':
        current_user.full_name     = request.form.get('full_name', '').strip()
        current_user.university    = request.form.get('university', '').strip()
        current_user.department    = request.form.get('department', '').strip()
        current_user.year_of_study = int(request.form.get('year_of_study', 1))
        current_user.bio           = request.form.get('bio', '').strip()
        new_pw = request.form.get('new_password', '').strip()
        if new_pw:
            if not current_user.check_password(request.form.get('current_password', '')):
                flash('Current password is incorrect.', 'danger')
                return render_template('profile/edit.html')
            current_user.set_password(new_pw)
        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file and file.filename and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{uuid.uuid4().hex}.{ext}"
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                current_user.profile_photo = filename
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile.view', user_id=current_user.id))
    return render_template('profile/edit.html')
