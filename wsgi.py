from app import create_app

# 開発サーバー用のエントリーポイント
app = create_app('dev')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
