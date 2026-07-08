from extensions import db
from datetime import datetime

class Request(db.Model):
    __tablename__ = 'requests'

    id           = db.Column(db.Integer, primary_key=True)
    skill_id     = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    teacher_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic        = db.Column(db.String(100))
    message      = db.Column(db.Text)
    status       = db.Column(db.String(20), default='pending')
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    chat    = db.relationship('Chat',   backref='request', uselist=False)
    reviews = db.relationship('Review', backref='request', lazy='dynamic')

    def __repr__(self):
        return f'<Request {self.id} status={self.status}>'
