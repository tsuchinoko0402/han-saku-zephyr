from flask import render_template, jsonify
from app.views.main import main_bp
from app.models import FileType, Tag, File, ManagerUser

@main_bp.route('/')
def index():
    """トップページのルート"""
    return render_template('index.html')

@main_bp.route('/about')
def about():
    """アバウトページのルート（例）"""
    return render_template('index.html', content="About Page")

@main_bp.route('/api/file-types')
def file_types():
    """ファイルタイプの一覧を返すAPI"""
    types = FileType.query.all()
    result = [{'id': t.id, 'extension': t.extension, 'description': t.description} for t in types]
    return jsonify(result)

@main_bp.route('/api/tags')
def tags():
    """タグの一覧を返すAPI"""
    all_tags = Tag.query.all()
    result = [{'id': t.id, 'name': t.name} for t in all_tags]
    return jsonify(result)
