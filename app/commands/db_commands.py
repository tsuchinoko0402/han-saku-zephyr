import os
import click
from flask import current_app
from flask.cli import with_appcontext
import pymysql


def get_db_connection():
    """データベース接続オブジェクトを返す"""
    db_url = current_app.config['SQLALCHEMY_DATABASE_URI']
    # mysql+pymysql://user:password@db:3306/flask_db の形式から情報を抽出
    prefix = "mysql+pymysql://"
    url = db_url[len(prefix):]
    
    user_pass, rest = url.split('@', 1)
    if ':' in user_pass:
        user, password = user_pass.split(':', 1)
    else:
        user = user_pass
        password = ''
    
    host_port, db_name = rest.split('/', 1)
    if ':' in host_port:
        host, port = host_port.split(':', 1)
        port = int(port)
    else:
        host = host_port
        port = 3306
    
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        charset='utf8mb4'
    )

def table_exists(cursor, schema, table):
    """指定されたテーブルが存在するかどうかを確認"""
    cursor.execute(f"""
        SELECT COUNT(*) 
        FROM information_schema.tables 
        WHERE table_schema = '{schema}' 
        AND table_name = '{table}'
    """)
    return cursor.fetchone()[0] > 0

@click.command('init-db')
@click.option('--force', is_flag=True, help='既存のスキーマを強制的に上書きする')
@click.option('--clean', is_flag=True, help='既存のデータを削除してからやり直す')
@with_appcontext
def init_db_command(force, clean):
    """SQLファイルからデータベースを初期化する"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # クリーンアップオプションが有効な場合
        if clean:
            try:
                cursor.execute("DROP DATABASE IF EXISTS documents")
                cursor.execute("DROP DATABASE IF EXISTS auth")
                connection.commit()
                click.echo("既存のデータベースを削除しました。")
            except Exception as e:
                click.echo(f"データベース削除中にエラーが発生: {e}")
        
        # SQLファイルのパスを取得
        base_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        sql_dir = os.path.join(base_dir, 'db', 'migrations')  # 新しいパスに変更
        
        # スキーマを作成
        with open(os.path.join(sql_dir, '01_create_schemas.sql'), 'r') as f:
            sql = f.read()
            for statement in sql.split(';'):
                if statement.strip():
                    cursor.execute(statement)
        
        # テーブルを作成
        with open(os.path.join(sql_dir, '02_create_tables.sql'), 'r') as f:
            sql = f.read()
            for statement in sql.split(';'):
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except Exception as e:
                        click.echo(f"エラー: {e}")
                        click.echo(f"SQL: {statement}")
                        if not force:
                            raise
        
        # サンプルデータを挿入
        with open(os.path.join(sql_dir, '03_insert_datas.sql'), 'r') as f:
            sql = f.read()
            for statement in sql.split(';'):
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except Exception as e:
                        click.echo(f"エラー: {e}")
                        click.echo(f"SQL: {statement}")
                        if not force:
                            raise
        
        connection.commit()
        click.echo('データベースが初期化されました。')
    except Exception as e:
        click.echo(f'エラーが発生しました: {e}')
    finally:
        cursor.close()
        connection.close()


def init_app(app):
    """アプリケーションにコマンドを登録"""
    app.cli.add_command(init_db_command)
