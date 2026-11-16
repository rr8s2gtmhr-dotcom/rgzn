from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from .config import settings

engine = create_async_engine(settings.database_url, echo=False, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    # 仅创建表结构，不创建数据库本身：
    # 本地开发时数据库 rgzn-ai 已由用户手动建立；
    # Railway 等 PaaS 由平台自动创建数据库并注入连接参数，应用无建库权限。
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
