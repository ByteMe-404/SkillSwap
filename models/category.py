from extensions import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'categories'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), unique=True, nullable=False)
    icon       = db.Column(db.String(50), default='ti-star')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    skills = db.relationship('Skill', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'
