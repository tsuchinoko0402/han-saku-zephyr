from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import config_by_name

# データベースの初期化
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='dev'):
    """
    アプリケーションファクトリ関数
    Args:
        config_name: 'dev', 'test', 'prod'のいずれか
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # データベースの初期化
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Blueprintsの登録
    from app.views.main import main_bp
    app.register_blueprint(main_bp)
    
    # 追加のBlueprintがあれば、ここで登録
    
    return app

# アプリケーションのインスタンスを作成（開発環境用）
app = create_app('dev')
