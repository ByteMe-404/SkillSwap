from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    full_name     = db.Column(db.String(150), nullable=False)
    email         = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    university    = db.Column(db.String(200), nullable=False)
    department    = db.Column(db.String(150), nullable=False)
    year_of_study = db.Column(db.Integer, nullable=False)
    bio           = db.Column(db.Text)
    profile_photo = db.Column(db.String(500))
    role          = db.Column(db.String(20), default='student')
    is_active     = db.Column(db.Boolean, default=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    
    skills             = db.relationship('Skill',   backref='owner',     lazy='dynamic', foreign_keys='Skill.user_id')
    sent_requests      = db.relationship('Request', backref='requester', lazy='dynamic', foreign_keys='Request.requester_id')
    received_requests  = db.relationship('Request', backref='teacher',   lazy='dynamic', foreign_keys='Request.teacher_id')
    reviews_given      = db.relationship('Review',  backref='reviewer',  lazy='dynamic', foreign_keys='Review.reviewer_id')
    reviews_received   = db.relationship('Review',  backref='reviewee',  lazy='dynamic', foreign_keys='Review.reviewee_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def avg_rating(self):
        reviews = self.reviews_received.all()
        if not reviews:
            return None
        return round(sum(r.rating for r in reviews) / len(reviews), 1)


