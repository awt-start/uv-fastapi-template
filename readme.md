 极简 FastAPI 项目模板说明文档  

---

# 🚀 极简 FastAPI 项目模板说明文档  
**—— 支持多数据库 + JWT 认证 + uv + ruff + Docker**

> 作者：芒星  
> 最后更新：2025年11月17日  
> 适用场景：副业 MVP / 开源项目 / 轻量级后端服务

---

## ✅ 核心特性

| 特性             | 说明                                                         |
| ---------------- | ------------------------------------------------------------ |
| **多数据库支持** | PostgreSQL / MySQL / SQLite（通过配置切换）                  |
| **JWT 认证**     | 基于 `python-jose` + `passlib`，含登录/注册/权限校验         |
| **极速依赖管理** | 使用 [`uv`](https://github.com/astral-sh/uv) 替代 pip，安装快 10-100 倍 |
| **代码质量保障** | 使用 [`ruff`](https://docs.astral.sh/ruff/) 实现 lint + format 一体化 |
| **容器化部署**   | 提供生产级 Dockerfile，安全、高效、可移植                    |
| **结构清晰**     | 分层架构（API / Service / Model / Schema），易于维护         |
| **测试友好**     | pytest + httpx 异步测试支持                                  |

---

## 🧰 技术栈

| 类别        | 组件                                                         |
| ----------- | ------------------------------------------------------------ |
| Web 框架    | `fastapi>=0.110.0`                                           |
| ASGI 服务器 | `uvicorn[standard]>=0.29.0`                                  |
| 配置管理    | `pydantic-settings>=2.0.0`                                   |
| ORM         | `sqlalchemy[asyncio]>=2.0.0`                                 |
| 数据库驱动  | `asyncpg`（PG） / `aiomysql`（MySQL） / `aiosqlite`（SQLite） |
| 迁移工具    | `alembic>=1.13.0`                                            |
| JWT 认证    | `python-jose[cryptography]>=3.3.0` + `passlib[bcrypt]>=1.7.4` |
| 开发工具    | `uv`（依赖） + `ruff`（代码质量）                            |
| 测试        | `pytest>=7.0.0` + `httpx>=0.25.0`                            |
| 部署        | Docker（基于 `python:3.11-slim`）                            |

---

## 🗂️ 项目结构

```bash
fastapi-starter/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # 配置（支持多数据库）
│   │   ├── database.py        # 动态数据库引擎
│   │   ├── security.py        # JWT 工具函数
│   │   └── deps.py            # 依赖注入（db, current_user）
│   ├── models/                # SQLAlchemy 模型
│   │   └── user.py
│   ├── schemas/               # Pydantic 模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── token.py
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py        # JWT 登录/注册
│   │       └── users.py       # 受保护路由示例
│   └── crud/                  # 数据库操作封装
│       └── user.py
├── alembic/
├── alembic.ini
├── tests/
│   └── test_auth.py
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── pyproject.toml             # ruff 配置
├── requirements.in            # 直接依赖声明
├── uv.lock                    # 依赖锁定文件（由 uv 生成）
└── Makefile                   # 开发快捷命令
```

---

## ⚙️ 配置多数据库支持

### 1. `.env` 示例
```env
# .env
APP_ENV=development
SECRET_KEY=your-super-secret-jwt-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 三选一：
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/mydb
# DATABASE_URL=mysql+aiomysql://user:pass@localhost/mydb
# DATABASE_URL=sqlite+aiosqlite:///./app.db
```

### 2. `app/core/config.py`
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "development"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
```

### 3. `app/core/database.py`（自动适配）
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 自动识别数据库类型
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=(settings.APP_ENV == "development"),
    connect_args=connect_args,
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

> ✅ **SQLite 注意**：需在 Alembic 中启用 `render_as_batch=True`（因 SQLite 不支持 ALTER）

---

## 🔐 JWT 认证实现

### 关键文件
- `app/core/security.py`：`verify_password`, `get_password_hash`, `create_access_token`
- `app/api/v1/auth.py`：`/login` 接口
- `app/core/deps.py`：`get_current_user` 依赖

### 示例：受保护路由
```python
# app/api/v1/users.py
from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.schemas.user import UserOut

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user
```

---

## 📦 依赖管理（uv）

### `requirements.in`
```txt
fastapi>=0.110.0
uvicorn[standard]>=0.29.0
pydantic-settings>=2.0.0
sqlalchemy[asyncio]>=2.0.0
asyncpg>=0.27.0
aiomysql>=0.2.0
aiosqlite>=0.20.0
alembic>=1.13.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
pytest>=7.0.0
httpx>=0.25.0
python-dotenv>=1.0.0
```

### 常用命令
```bash
uv lock          # 生成 uv.lock
uv sync          # 安装依赖（含 dev）
uv sync --frozen # 生产安装（严格锁定）
```

---

## 🧹 代码质量（ruff）

### `pyproject.toml`
```toml
[tool.ruff]
select = ["E", "W", "F", "I", "UP", "YTT"]
ignore = ["E501"]
line-length = 88

[tool.ruff.lint.isort]
known-first-party = ["app"]

[tool.ruff.format]
quote-style = "double"
```

### 命令
```bash
uv run ruff check .      # 检查
uv run ruff check --fix . && uv run ruff format .  # 修复+格式化
```

---

## 🐳 Docker 部署

### `Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app
RUN pip install uv

COPY requirements.in uv.lock ./
RUN uv sync --frozen --no-dev --no-editable

COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini .

RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 构建运行
```bash
docker build -t fastapi-app .
docker run -d -p 8000:8000 --env-file .env fastapi-app
```

---

## ▶️ 开发工作流（Makefile）

```makefile
install:
	uv sync

format:
	uv run ruff check --fix . && uv run ruff format .

test:
	uv run pytest

run:
	uv run uvicorn app.main:app --reload

docker-build:
	docker build -t fastapi-app .
```

---

## 📥 如何开始？

1. 安装 [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. 克隆模板（或按本文手动创建）
3. 配置 `.env`
4. 运行：
   ```bash
   make install
   make run
   ```
5. 访问 `http://localhost:8000/docs` 查看 Swagger

---

## 📚 后续扩展建议

| 需求            | 推荐方案                            |
| --------------- | ----------------------------------- |
| 异步任务        | `propan` 或 `celery`                |
| Prometheus 监控 | `prometheus-fastapi-instrumentator` |
| 邮件服务        | `smtplib` + `aiosmtplib`            |
| CORS            | `fastapi.middleware.cors`           |

---

## 📝 总结

这套方案在 **极简** 与 **工程化** 之间取得良好平衡：
- 启动快、依赖少，但结构清晰可维护（回应你对“FastAPI 维护性”的顾虑）
- 支持多数据库，适应不同部署环境（你使用 Linux 服务器，可自由选择 PG/MySQL/SQLite）
- JWT 认证开箱即用，适合用户系统
- `uv` + `ruff` + `Docker` 组合提升开发与部署效率

> 💡 **适合你当前目标**：作为副业或开源项目快速验证想法，同时具备向中大型项目演进的基础。

---

