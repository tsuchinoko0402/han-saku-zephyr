from flask import render_template, jsonify
from app.views.main import main_bp
from app.models import FileType, Tag, File, ManagerUser
from app import db
import sqlalchemy

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

@main_bp.route('/health')
def health_check():
    """
    アプリケーションとデータベースの状態を確認するヘルスチェックエンドポイント
    
    以下を確認:
    1. Flaskアプリケーションが応答すること
    2. データベース接続が機能していること
    """
    health_status = {
        'status': 'ok',
        'app': 'healthy',
        'database': 'unknown'
    }
    
    # データベース接続チェック
    try:
        # 単純なクエリでデータベース接続をテスト
        db.session.execute(sqlalchemy.text('SELECT 1'))
        health_status['database'] = 'connected'
    except Exception as e:
        health_status['status'] = 'error'
        health_status['database'] = 'disconnected'
        health_status['database_error'] = str(e)
    
    return jsonify(health_status)
