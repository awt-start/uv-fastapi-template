import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.user import Base, User


async def test_database():
    """测试数据库连接和表创建"""
    try:
        # 创建内存数据库引擎
        engine = create_async_engine(
            "sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False}
        )

        # 创建表
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("数据库表创建成功")

        # 创建会话并插入数据
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

        async with async_session() as session:
            # 检查是否有users表
            result = await session.execute("PRAGMA table_info(users)")
            columns = result.fetchall()
            print(f"Users表列: {columns}")

            # 插入测试数据
            user = User(
                email="test@example.com",
                full_name="Test User",
                hashed_password="hashed_password",
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            print(f"插入的用户: {user}")

        await engine.dispose()
        print("数据库连接关闭")

    except Exception as e:
        print(f"错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_database())
