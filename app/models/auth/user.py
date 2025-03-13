from app import db
from datetime import datetime

class ManagerUser(db.Model):
    __tablename__ = 'manager_users'
    __table_args__ = {'schema': 'auth'}
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_name = db.Column(db.String(100), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # ファイルとのリレーション（逆参照）
    created_files = db.relationship('File', foreign_keys='File.created_by', backref='creator')
    updated_files = db.relationship('File', foreign_keys='File.updated_by', backref='updater')
    
    def __repr__(self):
        return f'<ManagerUser {self.username}>'
