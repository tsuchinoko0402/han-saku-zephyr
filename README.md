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
  "documents.files" {
    int id PK
    varchar file_name
    varchar url
    boolean is_template
  }
  
  "documents.file_types" {
    int id PK
    varchar extension
  }
  
  "documents.tags" {
    int id PK
    varchar name
  }
  
  "documents.file_tags" {
    int file_id FK
    int tag_id FK
  }
  
  "auth.manager_users" {
    int id PK
    varchar username
    varchar role_name
  }
  
  "documents.files" ||--o{ "documents.file_tags" : "has"
  "documents.files" }|--|| "documents.file_types"  : "has_type"
  "documents.files" }|--|| "auth.manager_users" : "created_by"
  "documents.files" }|--|| "auth.manager_users" : "updated_by"
  "documents.file_tags" }|--|| "documents.tags" : "belongs_to"
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

## ドキュメント

- [技術仕様書](docs/TECHNICAL_SPECIFICATION.md) - アプリケーションの詳細な技術仕様と設計
