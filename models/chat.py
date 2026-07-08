from extensions import db
from datetime import datetime

class Chat(db.Model):
    __tablename__ = 'chats'

    id         = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), unique=True, nullable=False)
    user1_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user1    = db.relationship('User', foreign_keys=[user1_id])
    user2    = db.relationship('User', foreign_keys=[user2_id])
    messages = db.relationship('Message', backref='chat', lazy='dynamic', order_by='Message.created_at')

    def other_user(self, current_user_id):
        return self.user2 if self.user1_id == current_user_id else self.user1

    def last_message(self):
        from models.message import Message
        return self.messages.order_by(Message.created_at.desc()).first()

    def __repr__(self):
        return f'<Chat {self.id}>'
