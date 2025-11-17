# 使用官方 Python 3.10 镜像
FROM python:3.10-slim

# 设置环境变量，避免 Python 写入 .pyc 文件
ENV PYTHONDONTWRITEBYTECODE 1
# 确保 Python 输出直接发送到终端，方便查看日志
ENV PYTHONUNBUFFERED 1

# 设置工作目录
WORKDIR /app

# 1. 先安装系统依赖
#    将这一步与下面的依赖安装分开，可以利用 Docker 缓存。
#    只要这部分不改变，后续的步骤就可以使用缓存。
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. 安装 uv
RUN pip install --no-cache-dir uv

# 3. 复制依赖声明文件
COPY requirements.in uv.lock ./

# 4. 使用 uv 安装依赖
#    --frozen: 严格按照 uv.lock 安装，保证构建一致性
RUN uv sync --frozen --no-dev --no-editable --no-cache

# 5. 复制应用代码
#    将代码复制放在依赖安装之后，这样修改代码就不会导致依赖重新安装
COPY . .

# 创建非 root 用户（安全）
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查（可选：Docker 层面）
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]