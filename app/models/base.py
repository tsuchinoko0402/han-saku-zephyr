from datetime import datetime
from app import db

class Base(db.Model):
    """ベースモデルクラス"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """モデルインスタンスを保存"""
        db.session.add(self)
        db.session.commit()
        return self
