from app import db
from datetime import datetime

class FileType(db.Model):
    __tablename__ = 'file_types'
    __table_args__ = {'schema': 'documents'}
    
    id = db.Column(db.Integer, primary_key=True)
    extension = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    
    # ファイルとのリレーション
    files = db.relationship('File', backref='file_type')
    
    def __repr__(self):
        return f'<FileType {self.extension}>'
    

class Tag(db.Model):
    __tablename__ = 'tags'
    __table_args__ = {'schema': 'documents'}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    # 中間テーブルを通じたリレーション
    files = db.relationship('File', secondary='documents.file_tags', backref='tags')
    
    def __repr__(self):
        return f'<Tag {self.name}>'


# ファイルとタグの中間テーブル
file_tags = db.Table('file_tags',
    db.Column('file_id', db.Integer, db.ForeignKey('documents.files.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('documents.tags.id'), primary_key=True),
    schema='documents'
)


class File(db.Model):
    __tablename__ = 'files'
    __table_args__ = {'schema': 'documents'}
    
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(1000), nullable=False)
    file_type_id = db.Column(db.Integer, db.ForeignKey('documents.file_types.id'), nullable=False)
    file_size = db.Column(db.BigInteger, nullable=False)
    is_template = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('auth.manager_users.id'), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('auth.manager_users.id'), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<File {self.display_name}>'
