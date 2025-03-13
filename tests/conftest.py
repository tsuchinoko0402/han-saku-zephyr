import pytest
from app import create_app, db

@pytest.fixture
def app():
    """アプリケーションのテスト用フィクスチャ"""
    # テスト用の設定を使用
    app = create_app('test')
    
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
