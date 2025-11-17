# 构建阶段
FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY uv.lock requirements.txt ./
RUN uv pip install --system --no-cache -r requirements.txt --target /install

# 运行阶段
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 复制已安装的包
COPY --from=builder /install /usr/local/lib/python3.11/site-packages

COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini .

RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]