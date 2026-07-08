from extensions import db
from datetime import datetime
import json

class Skill(db.Model):
    __tablename__ = 'skills'

    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id      = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    title            = db.Column(db.String(80), nullable=False)
    short_desc       = db.Column(db.String(160), nullable=False)
    description      = db.Column(db.Text, nullable=False)
    level            = db.Column(db.String(20), default='Beginner')
    session_duration = db.Column(db.String(50), default='45-60 minutes')
    session_format   = db.Column(db.String(20), default='Both')
    max_students     = db.Column(db.Integer, default=1)
    _availability    = db.Column('availability', db.Text)
    _topics          = db.Column('topics', db.Text)
    _outcomes        = db.Column('outcomes', db.Text)
    status           = db.Column(db.String(10), default='draft')
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at       = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    requests = db.relationship('Request', backref='skill', lazy='dynamic')

    @property
    def availability(self):
        return json.loads(self._availability) if self._availability else []

    @availability.setter
    def availability(self, value):
        self._availability = json.dumps(value)

    @property
    def topics(self):
        return json.loads(self._topics) if self._topics else []

    @topics.setter
    def topics(self, value):
        self._topics = json.dumps(value)

    @property
    def outcomes(self):
        return json.loads(self._outcomes) if self._outcomes else []

    @outcomes.setter
    def outcomes(self, value):
        self._outcomes = json.dumps(value)

    def avg_rating(self):
        from models.review import Review
        from models.request import Request
        reviews = Review.query.join(Request).filter(Request.skill_id == self.id).all()
        if not reviews:
            return None
        return round(sum(r.rating for r in reviews) / len(reviews), 1)

    def review_count(self):
        from models.review import Review
        from models.request import Request
        return Review.query.join(Request).filter(Request.skill_id == self.id).count()

    def __repr__(self):
        return f'<Skill {self.title}>'
