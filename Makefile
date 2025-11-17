# 项目开发工作流命令

# 设置默认目标
.DEFAULT_GOAL := help

# 环境变量
VENV_DIR := .venv
PYTHON := $(VENV_DIR)/Scripts/python
UV := $(VENV_DIR)/Scripts/uv

# 帮助信息
.PHONY: help
help:
	@echo "可用命令："
	@echo "  make install      # 安装依赖"
	@echo "  make dev          # 启动开发服务器"
	@echo "  make test         # 运行测试"
	@echo "  make lint         # 代码检查"
	@echo "  make build        # 构建Docker镜像"
	@echo "  make run          # 运行Docker容器"
	@echo "  make clean        # 清理构建文件"

# 安装依赖
.PHONY: install
install:
	@if not exist $(VENV_DIR) (uv venv) endif
	@$(UV) pip install -r requirements.txt
	@echo "依赖安装完成！"
# 格式化
.PHONY: format
format:
	uv run ruff format .

# 启动开发服务器
.PHONY: dev
dev:
	@$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000

# 运行测试
.PHONY: test
test:
	@$(PYTHON) -m pytest tests/ -v

# 代码检查
.PHONY: lint
lint:
	@$(PYTHON) -m flake8 app/ tests/

# 构建Docker镜像
.PHONY: build
build:
	@docker build -t uv-fastapi-template .

# 运行Docker容器
.PHONY: run
run:
	@docker run -p 8000:8000 --env-file .env uv-fastapi-template

# 清理构建文件
.PHONY: clean
clean:
	@if exist "$(VENV_DIR)" rmdir /s /q "$(VENV_DIR)" endif
	@if exist "__pycache__" rmdir /s /q "__pycache__" endif
	@if exist "app/__pycache__" rmdir /s /q "app/__pycache__" endif
	@if exist "tests/__pycache__" rmdir /s /q "tests/__pycache__" endif
	@if exist "*.pyc" del /q "*.pyc" endif
	@if exist "app/*.pyc" del /q "app/*.pyc" endif
	@if exist "tests/*.pyc" del /q "tests/*.pyc" endif
	@echo "清理完成！"