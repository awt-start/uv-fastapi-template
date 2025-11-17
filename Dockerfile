# 使用官方 Python 3.10 镜像（你指定的版本）
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装 uv（现代 Python 包管理器）
RUN pip install --no-cache-dir uv

# 复制依赖声明文件
COPY requirements.in uv.lock ./

# 使用 uv 安装依赖（--frozen 确保锁定，--no-cache 节省空间）
RUN uv sync --frozen --no-dev --no-editable --no-cache

# 复制应用代码（排除本地虚拟环境等）
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