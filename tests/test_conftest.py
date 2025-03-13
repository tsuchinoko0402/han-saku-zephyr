import pytest
from app import create_app, db
from app.config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    """アプリケーションのテスト用フィクスチャ"""
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """テストクライアントのフィクスチャ"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """CLI テストランナーのフィクスチャ"""
    return app.test_cli_runner()
