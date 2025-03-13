from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from app.config import config_by_name

# データベースの初期化
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    """
    アプリケーションファクトリ関数
    Args:
        config_name: 'dev', 'test', 'prod'のいずれか
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'dev')
        
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # データベースの初期化
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Blueprintsの登録
    # 注意: このimportはcreate_app内で行う必要がある（循環インポート防止）
    from app.views.main import main_bp
    app.register_blueprint(main_bp)
    
    # デバッグ用にルートを出力
    print(f"Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")
    
    return app

# アプリケーションのインスタンスを直接作成しない
# wsgi.pyで作成する
