# ==========================================
# FastAPI 项目开发工作流
# ==========================================

# 项目配置
PROJECT_NAME := fastapi-template
VENV_DIR := .venv
PYTHON := $(VENV_DIR)/Scripts/python
UV := $(VENV_DIR)/Scripts/uv
PIP := $(VENV_DIR)/Scripts/pip

# 服务配置
HOST := 0.0.0.0
PORT := 5000
WORKERS := 4

# Docker 配置
DOCKER_IMAGE := $(PROJECT_NAME)
DOCKER_TAG := latest
DOCKER_FULL_IMAGE := $(DOCKER_IMAGE):$(DOCKER_TAG)

# 颜色输出
COLOR_RESET := \033[0m
COLOR_BLUE := \033[34m
COLOR_GREEN := \033[32m
COLOR_YELLOW := \033[33m

# 默认目标
.DEFAULT_GOAL := help

# ==========================================
# 帮助信息
# ==========================================
.PHONY: help
help:
    @echo "$(COLOR_BLUE)=========================================$(COLOR_RESET)"
    @echo "$(COLOR_BLUE)=========================================$(COLOR_RESET)"
    @echo ""
    @echo "$(COLOR_GREEN)环境管理:$(COLOR_RESET)"
    @echo "  make setup        # 初始化项目环境（创建虚拟环境+安装依赖）"
    @echo "  make install      # 安装/更新依赖"
    @echo "  make upgrade      # 升级所有依赖到最新版本"
    @echo ""
    @echo "$(COLOR_GREEN)开发:$(COLOR_RESET)"
    @echo "  make dev          # 启动开发服务器（热重载）"
    @echo "  make run          # 启动生产服务器"
    @echo "  make shell        # 进入 Python 交互式环境"
    @echo ""
    @echo "$(COLOR_GREEN)代码质量:$(COLOR_RESET)"
    @echo "  make format       # 格式化代码"
    @echo "  make lint         # 代码检查"
    @echo "  make type-check   # 类型检查"
    @echo "  make check        # 运行所有检查（格式+lint+类型）"
    @echo ""
    @echo "$(COLOR_GREEN)测试:$(COLOR_RESET)"
    @echo "  make test         # 运行测试"
    @echo "  make test-cov     # 运行测试并生成覆盖率报告"
    @echo "  make test-watch   # 监视模式运行测试"
    @echo ""
    @echo "$(COLOR_GREEN)Docker:$(COLOR_RESET)"
    @echo "  make docker-build # 构建 Docker 镜像"
    @echo "  make docker-run   # 运行 Docker 容器"
    @echo "  make docker-stop  # 停止 Docker 容器"
    @echo "  make docker-logs  # 查看 Docker 日志"
    @echo ""
    @echo "$(COLOR_GREEN)数据库:$(COLOR_RESET)"
    @echo "  make db-migrate   # 生成数据库迁移"
    @echo "  make db-upgrade   # 应用数据库迁移"
    @echo "  make db-reset     # 重置数据库"
    @echo ""
    @echo "$(COLOR_GREEN)清理:$(COLOR_RESET)"
    @echo "  make clean        # 清理缓存和临时文件"
    @echo "  make clean-all    # 清理所有（包括虚拟环境）"
    @echo ""

# ==========================================
# 环境管理
# ==========================================
.PHONY: setup
setup: clean-all
    @echo "$(COLOR_BLUE)创建虚拟环境...$(COLOR_RESET)"
    @uv venv
    @echo "$(COLOR_BLUE)安装依赖...$(COLOR_RESET)"
    @$(UV) pip install -r requirements.txt
    @echo "$(COLOR_GREEN)✓ 环境初始化完成！$(COLOR_RESET)"

.PHONY: install
install:
    @echo "$(COLOR_BLUE)安装依赖...$(COLOR_RESET)"
    @if not exist $(VENV_DIR) (uv venv)
    @$(UV) pip install -r requirements.txt
    @echo "$(COLOR_GREEN)✓ 依赖安装完成！$(COLOR_RESET)"

.PHONY: upgrade
upgrade:
    @echo "$(COLOR_BLUE)升级依赖...$(COLOR_RESET)"
    @$(UV) pip install --upgrade -r requirements.txt
    @echo "$(COLOR_GREEN)✓ 依赖升级完成！$(COLOR_RESET)"

# ==========================================
# 开发
# ==========================================
.PHONY: dev
dev:
    @echo "$(COLOR_BLUE)启动开发服务器...$(COLOR_RESET)"
    @$(PYTHON) -m uvicorn app.main:app --reload --host $(HOST) --port $(PORT)

.PHONY: run
run:
    @echo "$(COLOR_BLUE)启动生产服务器...$(COLOR_RESET)"
    @$(PYTHON) -m uvicorn app.main:app --host $(HOST) --port $(PORT) --workers $(WORKERS)

.PHONY: shell
shell:
    @echo "$(COLOR_BLUE)进入 Python 交互式环境...$(COLOR_RESET)"
    @$(PYTHON)

# ==========================================
# 代码质量
# ==========================================
.PHONY: format
format:
    @echo "$(COLOR_BLUE)格式化代码...$(COLOR_RESET)"
    @$(PYTHON) -m ruff format .
    @$(PYTHON) -m ruff check --fix .
    @echo "$(COLOR_GREEN)✓ 代码格式化完成！$(COLOR_RESET)"

.PHONY: lint
lint:
    @echo "$(COLOR_BLUE)运行代码检查...$(COLOR_RESET)"
    @$(PYTHON) -m ruff check .
    @echo "$(COLOR_GREEN)✓ 代码检查完成！$(COLOR_RESET)"

.PHONY: type-check
type-check:
    @echo "$(COLOR_BLUE)运行类型检查...$(COLOR_RESET)"
    @$(PYTHON) -m mypy app/ --ignore-missing-imports
    @echo "$(COLOR_GREEN)✓ 类型检查完成！$(COLOR_RESET)"

.PHONY: check
check: format lint type-check
    @echo "$(COLOR_GREEN)✓ 所有检查通过！$(COLOR_RESET)"

# ==========================================
# 测试
# ==========================================
.PHONY: test
test:
    @echo "$(COLOR_BLUE)运行测试...$(COLOR_RESET)"
    @$(PYTHON) -m pytest tests/ -v

.PHONY: test-cov
test-cov:
    @echo "$(COLOR_BLUE)运行测试并生成覆盖率报告...$(COLOR_RESET)"
    @$(PYTHON) -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term
    @echo "$(COLOR_GREEN)✓ 覆盖率报告已生成：htmlcov/index.html$(COLOR_RESET)"

.PHONY: test-watch
test-watch:
    @echo "$(COLOR_BLUE)监视模式运行测试...$(COLOR_RESET)"
    @$(PYTHON) -m pytest-watch tests/ -v

# ==========================================
# Docker
# ==========================================
.PHONY: docker-build
docker-build:
    @echo "$(COLOR_BLUE)构建 Docker 镜像...$(COLOR_RESET)"
    @docker build -t $(DOCKER_FULL_IMAGE) .
    @echo "$(COLOR_GREEN)✓ 镜像构建完成：$(DOCKER_FULL_IMAGE)$(COLOR_RESET)"

.PHONY: docker-run
docker-run:
    @echo "$(COLOR_BLUE)运行 Docker 容器...$(COLOR_RESET)"
    @docker run -d --name $(PROJECT_NAME) -p $(PORT):8000 --env-file .env $(DOCKER_FULL_IMAGE)
    @echo "$(COLOR_GREEN)✓ 容器已启动：http://localhost:$(PORT)$(COLOR_RESET)"

.PHONY: docker-stop
docker-stop:
    @echo "$(COLOR_BLUE)停止 Docker 容器...$(COLOR_RESET)"
    @docker stop $(PROJECT_NAME) 2>nul || echo "容器未运行"
    @docker rm $(PROJECT_NAME) 2>nul || echo "容器已清理"
    @echo "$(COLOR_GREEN)✓ 容器已停止$(COLOR_RESET)"

.PHONY: docker-logs
docker-logs:
    @docker logs -f $(PROJECT_NAME)

.PHONY: docker-shell
docker-shell:
    @docker exec -it $(PROJECT_NAME) /bin/bash

# ==========================================
# 数据库
# ==========================================
.PHONY: db-migrate
db-migrate:
    @echo "$(COLOR_BLUE)生成数据库迁移...$(COLOR_RESET)"
    @$(PYTHON) -m alembic revision --autogenerate -m "$(msg)"
    @echo "$(COLOR_GREEN)✓ 迁移文件已生成$(COLOR_RESET)"

.PHONY: db-upgrade
db-upgrade:
    @echo "$(COLOR_BLUE)应用数据库迁移...$(COLOR_RESET)"
    @$(PYTHON) -m alembic upgrade head
    @echo "$(COLOR_GREEN)✓ 数据库已更新$(COLOR_RESET)"

.PHONY: db-reset
db-reset:
    @echo "$(COLOR_YELLOW)警告：这将删除所有数据！$(COLOR_RESET)"
    @$(PYTHON) -m alembic downgrade base
    @$(PYTHON) -m alembic upgrade head
    @echo "$(COLOR_GREEN)✓ 数据库已重置$(COLOR_RESET)"

# ==========================================
# 清理
# ==========================================
.PHONY: clean
clean:
    @echo "$(COLOR_BLUE)清理缓存和临时文件...$(COLOR_RESET)"
    @if exist "__pycache__" rmdir /s /q "__pycache__" 2>nul
    @if exist "app/__pycache__" rmdir /s /q "app/__pycache__" 2>nul
    @if exist "tests/__pycache__" rmdir /s /q "tests/__pycache__" 2>nul
    @if exist ".pytest_cache" rmdir /s /q ".pytest_cache" 2>nul
    @if exist ".mypy_cache" rmdir /s /q ".mypy_cache" 2>nul
    @if exist ".ruff_cache" rmdir /s /q ".ruff_cache" 2>nul
    @if exist "htmlcov" rmdir /s /q "htmlcov" 2>nul
    @if exist ".coverage" del /q ".coverage" 2>nul
    @if exist "*.pyc" del /s /q "*.pyc" 2>nul
    @echo "$(COLOR_GREEN)✓ 清理完成！$(COLOR_RESET)"

.PHONY: clean-all
clean-all: clean
    @echo "$(COLOR_BLUE)清理虚拟环境...$(COLOR_RESET)"
    @if exist "$(VENV_DIR)" rmdir /s /q "$(VENV_DIR)" 2>nul
    @echo "$(COLOR_GREEN)✓ 完全清理完成！$(COLOR_RESET)"

# ==========================================
# 工具命令
# ==========================================
.PHONY: show-routes
show-routes:
    @echo "$(COLOR_BLUE)显示所有路由...$(COLOR_RESET)"
    @$(PYTHON) -c "from app.main import app; print('\n'.join(f'{r.methods} {r.path}' for r in app.routes))"

.PHONY: requirements
requirements:
    @echo "$(COLOR_BLUE)导出依赖列表...$(COLOR_RESET)"
    @$(UV) pip freeze > requirements.txt
    @echo "$(COLOR_GREEN)✓ 依赖已导出到 requirements.txt$(COLOR_RESET)"