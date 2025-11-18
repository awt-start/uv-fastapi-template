import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.base import Base
from app.core.deps import get_db


@pytest.mark.asyncio
async def test_create_student():
    """测试创建学生"""
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
        # 创建测试客户端
        async with AsyncClient(app=app, base_url="http://test") as client:
            # 首先注册并登录用户获取JWT令牌
            await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "test@example.com",
                    "password": "testpassword123",
                    "full_name": "Test User",
                },
            )
            login_response = await client.post(
                "/api/v1/auth/login",
                data={"username": "test@example.com", "password": "testpassword123"},
            )
            token = login_response.json()["access_token"]

            # 创建学生
            student_data = {
                "student_id": "20230001",
                "name": "张三",
                "age": 20,
                "gender": "男",
                "major": "计算机科学与技术",
                "email": "zhangsan@example.com",
            }
            response = await client.post(
                "/api/v1/students/",
                json=student_data,
                headers={"Authorization": f"Bearer {token}"},
            )
            assert response.status_code == 201
            assert response.json()["student_id"] == student_data["student_id"]
            assert response.json()["name"] == student_data["name"]
    finally:
        # 清理资源
        app.dependency_overrides.clear()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest.mark.asyncio
async def test_get_students():
    """测试获取学生列表"""
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
        # 创建测试客户端
        async with AsyncClient(app=app, base_url="http://test") as client:
            # 首先注册并登录用户获取JWT令牌
            await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "test@example.com",
                    "password": "testpassword123",
                    "full_name": "Test User",
                },
            )
            login_response = await client.post(
                "/api/v1/auth/login",
                data={"username": "test@example.com", "password": "testpassword123"},
            )
            token = login_response.json()["access_token"]

            # 创建两个学生用于测试
            student1_data = {
                "student_id": "20230001",
                "name": "张三",
                "age": 20,
                "gender": "男",
                "major": "计算机科学与技术",
                "email": "zhangsan@example.com",
            }
            student2_data = {
                "student_id": "20230002",
                "name": "李四",
                "age": 21,
                "gender": "女",
                "major": "软件工程",
                "email": "lisi@example.com",
            }
            await client.post(
                "/api/v1/students/",
                json=student1_data,
                headers={"Authorization": f"Bearer {token}"},
            )
            await client.post(
                "/api/v1/students/",
                json=student2_data,
                headers={"Authorization": f"Bearer {token}"},
            )

            # 获取学生列表
            response = await client.get(
                "/api/v1/students/", headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200
            students = response.json()
            assert len(students) == 2
    finally:
        # 清理资源
        app.dependency_overrides.clear()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest.mark.asyncio
async def test_get_student():
    """测试根据ID获取学生信息"""
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
        # 创建测试客户端
        async with AsyncClient(app=app, base_url="http://test") as client:
            # 首先注册并登录用户获取JWT令牌
            await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "test@example.com",
                    "password": "testpassword123",
                    "full_name": "Test User",
                },
            )
            login_response = await client.post(
                "/api/v1/auth/login",
                data={"username": "test@example.com", "password": "testpassword123"},
            )
            token = login_response.json()["access_token"]

            # 创建学生
            student_data = {
                "student_id": "20230001",
                "name": "张三",
                "age": 20,
                "gender": "男",
                "major": "计算机科学与技术",
                "email": "zhangsan@example.com",
            }
            create_response = await client.post(
                "/api/v1/students/",
                json=student_data,
                headers={"Authorization": f"Bearer {token}"},
            )
            student_id = create_response.json()["id"]

            # 根据ID获取学生信息
            response = await client.get(
                f"/api/v1/students/{student_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert response.status_code == 200
            assert response.json()["id"] == student_id
            assert response.json()["name"] == student_data["name"]
    finally:
        # 清理资源
        app.dependency_overrides.clear()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest.mark.asyncio
async def test_update_student():
    """测试更新学生信息"""
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
        # 创建测试客户端
        async with AsyncClient(app=app, base_url="http://test") as client:
            # 首先注册并登录用户获取JWT令牌
            await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "test@example.com",
                    "password": "testpassword123",
                    "full_name": "Test User",
                },
            )
            login_response = await client.post(
                "/api/v1/auth/login",
                data={"username": "test@example.com", "password": "testpassword123"},
            )
            token = login_response.json()["access_token"]

            # 创建学生
            student_data = {
                "student_id": "20230001",
                "name": "张三",
                "age": 20,
                "gender": "男",
                "major": "计算机科学与技术",
                "email": "zhangsan@example.com",
            }
            create_response = await client.post(
                "/api/v1/students/",
                json=student_data,
                headers={"Authorization": f"Bearer {token}"},
            )
            student_id = create_response.json()["id"]

            # 更新学生信息
            update_data = {"name": "张三三", "age": 21, "major": "人工智能"}
            response = await client.put(
                f"/api/v1/students/{student_id}",
                json=update_data,
                headers={"Authorization": f"Bearer {token}"},
            )
            assert response.status_code == 200
            assert response.json()["id"] == student_id
            assert response.json()["name"] == update_data["name"]
            assert response.json()["age"] == update_data["age"]
            assert response.json()["major"] == update_data["major"]
    finally:
        # 清理资源
        app.dependency_overrides.clear()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest.mark.asyncio
async def test_delete_student():
    """测试删除学生信息"""
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
        # 创建测试客户端
        async with AsyncClient(app=app, base_url="http://test") as client:
            # 首先注册并登录用户获取JWT令牌
            await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "test@example.com",
                    "password": "testpassword123",
                    "full_name": "Test User",
                },
            )
            login_response = await client.post(
                "/api/v1/auth/login",
                data={"username": "test@example.com", "password": "testpassword123"},
            )
            token = login_response.json()["access_token"]

            # 创建学生
            student_data = {
                "student_id": "20230001",
                "name": "张三",
                "age": 20,
                "gender": "男",
                "major": "计算机科学与技术",
                "email": "zhangsan@example.com",
            }
            create_response = await client.post(
                "/api/v1/students/",
                json=student_data,
                headers={"Authorization": f"Bearer {token}"},
            )
            student_id = create_response.json()["id"]

            # 删除学生
            response = await client.delete(
                f"/api/v1/students/{student_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert response.status_code == 204

            # 验证学生是否已删除
            get_response = await client.get(
                f"/api/v1/students/{student_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert get_response.status_code == 404
    finally:
        # 清理资源
        app.dependency_overrides.clear()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()
