FROM python:3.8.20-slim

WORKDIR /app

# 依存関係のインストール
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    git \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Poetryのインストール
RUN pip install poetry==1.7.1 black flake8 pytest

# 依存関係のコピーとインストール
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# アプリケーションのコピーと実行
COPY . .

EXPOSE 5000

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
