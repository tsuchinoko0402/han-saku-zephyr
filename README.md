# han-saku-zephyr
阪神さくら地区加盟員向けシステム

## 要件

- Python 3.8.20
- MySQL 8.0
- Docker と Docker Compose
- Poetry (パッケージ管理)

## ER図

```mermaid
erDiagram
  files {
    int id PK
    varchar file_name "ファイル名"
    varchar display_name "表示名"
    varchar url "URL"
    int file_type_id FK "ファイル形式"
    bigint file_size "ファイルサイズ(バイト)"
    boolean is_template "定型文書か否か"
    datetime created_at "作成日時"
    int created_by FK "作成者ID"
    datetime updated_at "更新日時" 
    int updated_by FK "更新者ID"
    datetime deleted_at "削除日時（ソフトデリート用）"
  }
  
  file_types {
    int id PK
    varchar extension "ファイルの拡張子"
    varchar description "拡張子の説明"
  }
  
  file_tags {
    int file_id FK "fileのid"
    int tag_id FK "タグid"
  }
  
  tags {
    int id PK
    varchar name "タグ名"
  }
  
  auth.manager_users {
    int id PK
    varchar username "ユーザー名"
    varchar password_hash "ハッシュ化パスワード"
    varchar role_name "役務名"
    datetime last_login "最終ログイン日時"
    datetime created_at "作成日時"
    datetime updated_at "更新日時"
  }
  
  files ||--o{ file_tags : "has"
  files }|--|| file_types : "has_type"
  files }|--|| auth.manager_users : "created_by"
  files }|--|| auth.manager_users : "updated_by"
  file_tags }|--|| tags : "belongs_to"
```

## セットアップ方法

### 開発環境の起動

```bash
# Docker Composeでアプリとデータベースを起動
docker-compose up -d

# マイグレーションの実行
docker-compose run --rm migration
```

### テストの実行

```bash
docker-compose run --rm web poetry run pytest
```

## プロジェクト構成

- `app/`: アプリケーションのメインコード
  - `models/`: データモデル
  - `templates/`: HTMLテンプレート
  - `views/`: ビューコントローラー
- `migrations/`: データベースマイグレーションファイル
- `tests/`: テストコード

## 本番環境

本番環境ではCGIを使用してアプリケーションを起動します。`index.cgi`が起動スクリプトとして機能します。
