"""
アプリケーションのヘルスチェック機能
"""
from flask import Blueprint, jsonify, current_app
from app import db
import sqlalchemy
import os
import platform
import sys
import time

# ヘルスチェック用のBlueprintを作成
health_bp = Blueprint('health', __name__, url_prefix='/health')

@health_bp.route('/')
def health_check():
    """基本的なヘルスチェック - アプリとDBの状態を確認"""
    start_time = time.time()
    
    health_status = {
        'status': 'ok',
        'app': 'healthy',
        'database': 'unknown',
        'timestamp': time.time()
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
    
    # レスポンスタイムを計算
    health_status['response_time_ms'] = round((time.time() - start_time) * 1000, 2)
    
    # Content-Typeを明示的に指定してJSONレスポンスを返す
    response = jsonify(health_status)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response

@health_bp.route('/detailed')
def detailed_health_check():
    """詳細なヘルスチェック - システム情報も含む"""
    start_time = time.time()
    
    health_status = {
        'status': 'ok',
        'app': {
            'status': 'healthy',
            'environment': current_app.config.get('ENV', 'unknown'),
            'debug_mode': current_app.debug,
            'python_version': sys.version,
            'platform': platform.platform()
        },
        'database': {
            'status': 'unknown'
        },
        'timestamp': time.time()
    }
    
    # データベース接続チェック
    try:
        # データベース情報を取得
        db_info = db.session.execute(sqlalchemy.text('SELECT VERSION()')).scalar()
        health_status['database'] = {
            'status': 'connected',
            'version': db_info
        }
        
        # スキーマ情報を取得
        try:
            schemas = db.session.execute(sqlalchemy.text(
                "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME IN ('documents', 'auth')"
            )).fetchall()
            health_status['database']['schemas'] = [schema[0] for schema in schemas]
        except Exception as e:
            health_status['database']['schemas_error'] = str(e)
        
    except Exception as e:
        health_status['status'] = 'error'
        health_status['database'] = {
            'status': 'disconnected',
            'error': str(e)
        }
    
    # メモリ使用量（概算）
    try:
        import psutil
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        health_status['system'] = {
            'memory_usage_mb': round(memory_info.rss / (1024 * 1024), 2)
        }
    except ImportError:
        # psutilがインストールされていない場合はこの情報はスキップ
        health_status['system'] = {
            'memory_usage': 'psutil not installed'
        }
    
    # レスポンスタイムを計算
    health_status['response_time_ms'] = round((time.time() - start_time) * 1000, 2)
    
    return jsonify(health_status)

def init_app(app):
    """アプリケーションにヘルスチェックBlueprintを登録"""
    app.register_blueprint(health_bp)
    
    # psutilのインストールを試みる（詳細なシステム情報用・オプション）
    try:
        import pip
        pip.main(['install', 'psutil'])
    except:
        app.logger.warning("psutilのインストールに失敗しました。詳細なシステムメトリクスは利用できません。")
