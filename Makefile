# 项目开发工作流命令

# 设置默认目标
.DEFAULT_GOAL := help

# 环境变量
VENV_DIR := .venv
PYTHON := $(VENV_DIR)/Scripts/python
UV := $(VENV_DIR)/Scripts/uv
PORT := 8000

# 帮助信息
.PHONY: help
help:
	@echo "可用命令："
	@echo "  make install          # 安装依赖"
	@echo "  make dev              # 启动开发服务器"
	@echo "  make test             # 运行测试"
	@echo "  make lint             # 代码检查"
	@echo "  make build            # 构建Docker镜像"
	@echo "  make run              # 运行Docker容器"
	@echo "  make clean            # 清理构建文件"
	@echo "  make migrate          # 生成新的数据库迁移脚本"
	@echo "  make migrate-upgrade  # 应用所有未应用的数据库迁移"
	@echo "  make migrate-downgrade # 回滚上一次数据库迁移"
	@echo "  make migrate-history  # 显示数据库迁移历史"
	@echo "  make migrate-init     # 初始化数据库迁移环境"

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
	@$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port $(PORT)

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

# 数据库迁移：生成新的迁移脚本
.PHONY: migrate
migrate:
	@echo "生成数据库迁移脚本..."
	@set PYTHONPATH=.; $(PYTHON) -m alembic revision --autogenerate -m "Automatic migration"
	@echo "迁移脚本生成完成！"

# 数据库迁移：应用所有未应用的迁移
.PHONY: migrate-upgrade
migrate-upgrade:
	@echo "应用数据库迁移..."
	@set PYTHONPATH=.; $(PYTHON) -m alembic upgrade head
	@echo "数据库迁移应用完成！"

# 数据库迁移：回滚上一次迁移
.PHONY: migrate-downgrade
migrate-downgrade:
	@echo "回滚数据库迁移..."
	@set PYTHONPATH=.; $(PYTHON) -m alembic downgrade -1
	@echo "数据库迁移回滚完成！"

# 数据库迁移：显示迁移历史
.PHONY: migrate-history
migrate-history:
	@echo "数据库迁移历史："
	@set PYTHONPATH=.; $(PYTHON) -m alembic history

# 数据库迁移：初始化迁移环境
.PHONY: migrate-init
migrate-init:
	@echo "初始化数据库迁移环境..."
	@$(PYTHON) -m alembic init alembic
	@echo "数据库迁移环境初始化完成！"

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