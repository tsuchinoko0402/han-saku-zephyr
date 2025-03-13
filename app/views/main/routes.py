from flask import render_template
from app.views.main import main_bp

@main_bp.route('/')
def index():
    """トップページのルート"""
    return render_template('index.html')

@main_bp.route('/about')
def about():
    """アバウトページのルート（例）"""
    return render_template('index.html', content="About Page")
