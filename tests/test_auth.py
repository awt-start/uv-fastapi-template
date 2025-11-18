import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.user import Base
from app.core.deps import get_db


@pytest.mark.asyncio
async def test_register():
    """测试用户注册"""
    # 创建独立的测试数据库引擎
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False}
    )

    # 创建表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 创建会话工厂
    TestingSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # 依赖函数
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    # 配置依赖
    app.dependency_overrides[get_db] = override_get_db

    try:
        # 创建测试客户端并运行测试
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "test_new@example.com",
                    "password": "testpassword123",
                    "full_name": "Test User",
                },
            )
            assert response.status_code == 200
            assert response.json()["email"] == "test_new@example.com"
    finally:
        # 清理资源
        app.dependency_overrides.clear()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest.mark.asyncio
async def test_login():
    """测试用户登录"""
    # 创建独立的测试数据库引擎
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False}
    )

    # 创建表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 创建会话工厂
    TestingSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # 依赖函数
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    # 配置依赖
    app.dependency_overrides[get_db] = override_get_db

    try:
        # 创建测试客户端并运行测试
        async with AsyncClient(app=app, base_url="http://test") as client:
            # 先注册用户
            await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "test@example.com",
                    "password": "testpassword123",
                    "full_name": "Test User",
                },
            )

            # 然后登录
            response = await client.post(
                "/api/v1/auth/login",
                data={"username": "test@example.com", "password": "testpassword123"},
            )
            assert response.status_code == 200
            assert "access_token" in response.json()
    finally:
        # 清理资源
        app.dependency_overrides.clear()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    """测试无效凭据登录"""
    # 创建独立的测试数据库引擎
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False}
    )

    # 创建表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 创建会话工厂
    TestingSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # 依赖函数
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    # 配置依赖
    app.dependency_overrides[get_db] = override_get_db

    try:
        # 创建测试客户端并运行测试
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/login",
                data={
                    "username": "nonexistent@example.com",
                    "password": "wrongpassword",
                },
            )
            assert response.status_code == 401
    finally:
        # 清理资源
        app.dependency_overrides.clear()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest.mark.asyncio
async def test_get_current_user():
    """测试获取当前用户信息"""
    # 创建独立的测试数据库引擎
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False}
    )

    # 创建表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 创建会话工厂
    TestingSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # 依赖函数
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    # 配置依赖
    app.dependency_overrides[get_db] = override_get_db

    try:
        # 创建测试客户端并运行测试
        async with AsyncClient(app=app, base_url="http://test") as client:
            # 注册用户
            await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "test@example.com",
                    "password": "testpassword123",
                    "full_name": "Test User",
                },
            )

            # 登录获取token
            login_response = await client.post(
                "/api/v1/auth/login",
                data={"username": "test@example.com", "password": "testpassword123"},
            )
            token = login_response.json()["access_token"]

            # 使用token获取当前用户信息
            response = await client.get(
                "/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200
            assert response.json()["email"] == "test@example.com"
            assert response.json()["full_name"] == "Test User"
    finally:
        # 清理资源
        app.dependency_overrides.clear()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()