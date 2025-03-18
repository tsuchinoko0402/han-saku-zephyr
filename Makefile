# han-saku-zephyr プロジェクト用 Makefile
# 様々なコマンドを簡単に実行するためのユーティリティ

.PHONY: help build up down restart logs shell test lint migrate init-db clean

# デフォルトのターゲット
help:
	@echo "利用可能なコマンド:"
	@echo "  make build      - Docker イメージをビルドする"
	@echo "  make up         - Docker コンテナを起動する"
	@echo "  make down       - Docker コンテナを停止する"
	@echo "  make restart    - Docker コンテナを再起動する"
	@echo "  make logs       - コンテナのログを表示する"
	@echo "  make shell      - Web コンテナ内でシェルを実行する"
	@echo "  make test       - テストを実行する"
	@echo "  make lint       - コードの静的解析を実行する"
	@echo "  make migrate    - データベースマイグレーションを実行する"
	@echo "  make init-db    - データベースを初期化する"
	@echo "  make init-db-clean - データベースをクリーンアップして初期化する"
	@echo "  make clean      - 一時ファイルを削除してクリーンアップする"

# Docker イメージをビルドする
build:
	docker compose build

# Docker コンテナを起動する
up:
	docker compose up -d

# Docker コンテナを停止する
down:
	docker compose down

# Docker コンテナを再起動する
restart:
	docker compose restart

# コンテナのログを表示する
logs:
	docker compose logs -f

# Web コンテナ内でシェルを実行する
shell:
	docker compose exec web /bin/bash

# テストを実行する
test:
	docker compose run --rm web poetry run pytest

# コードの静的解析を実行する
lint:
	docker compose run --rm web poetry run flake8

# データベースマイグレーションを実行する
migrate:
	docker compose run --rm web poetry run flask db upgrade

# データベースを初期化する
init-db:
	docker compose run --rm web poetry run flask init-db

# データベースをクリーンアップして初期化する
init-db-clean:
	docker compose run --rm web poetry run flask init-db --clean

# 一時ファイルを削除してクリーンアップする
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".DS_Store" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +
	find . -type f -name ".coverage.*" -delete
