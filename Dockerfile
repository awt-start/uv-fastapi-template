# 使用官方 Python 3.11 镜像
FROM python:3.11-slim

# 设置环境变量，避免 Python 写入 .pyc 文件
ENV PYTHONDONTWRITEBYTECODE 1
# 确保 Python 输出直接发送到终端，方便查看日志
ENV PYTHONUNBUFFERED 1

# 设置工作目录
WORKDIR /app

# 1. 先安装系统依赖（用于编译 C 扩展，如 asyncpg）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. 安装 uv（用于更快的依赖安装）
RUN pip install --no-cache-dir uv

# 3. 复制依赖锁定文件（必须先复制，利用 Docker 缓存）
COPY uv.lock requirements.txt ./

# 4. 使用 uv 安装依赖（生产模式）
#    --system: 直接安装到系统环境，而非虚拟环境
#    --no-cache: 不使用缓存，确保干净安装
RUN uv pip install --system --no-cache -r requirements.txt

# 5. 复制应用代码（只复制必要的）
COPY ./app ./app

# 6. 可选：复制 alembic 相关文件（如果存在）
# COPY ./alembic.ini ./alembic.ini
# COPY ./alembic ./alembic

# 7. 创建非 root 用户（安全）
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查（可选：Docker 层面）
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]