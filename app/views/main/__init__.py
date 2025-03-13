from flask import Blueprint

# main_bpという名前のBlueprintを作成
main_bp = Blueprint('main', __name__, url_prefix='/', template_folder='../../templates/main')

# ルーティングをインポート（循環インポートを避けるため）
from app.views.main import routes
