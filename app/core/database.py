from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 自动识别数据库类型，为SQLite添加特殊配置
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

# 创建异步数据库引擎
# 为SQLite添加异步驱动支持
database_url = settings.DATABASE_URL
if "sqlite://" in database_url:
    database_url = database_url.replace("sqlite://", "sqlite+aiosqlite://")

engine = create_async_engine(
    database_url,
    echo=(settings.APP_ENV == "development"),  # 开发环境下打印SQL语句
    connect_args=connect_args,
)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    """获取数据库会话依赖"""
    async with AsyncSessionLocal() as session:
        yield session
