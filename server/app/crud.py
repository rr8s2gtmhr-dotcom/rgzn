from typing import Any, Dict, List, Optional, Type
from sqlalchemy import select, func, or_, inspect
from sqlalchemy.ext.asyncio import AsyncSession

from . import models


RESOURCE_MODELS: Dict[str, Type[Any]] = {
    "menus": models.Menu,
    "units": models.Unit,
    "roles": models.Role,
    "users": models.User,
    "relarders": models.Relarder,
    "detections": models.Detection,
    "maintains": models.Maintain,
    "deldatas": models.Deldatas,
}

SEARCHABLE: Dict[str, List[str]] = {
    "menus": ["name", "path"],
    "units": ["deptName", "deptShortName"],
    "roles": ["roleName", "code"],
    "users": ["userName", "realName", "phone"],
    "relarders": ["deviceNo", "factory", "model", "address", "trackNo"],
    "detections": ["relarderNo", "trackNo", "detector"],
    "maintains": ["relarderNo", "maintainProject", "maintainUser"],
    "deldatas": ["relarderNo", "topNo", "unit", "yard", "track"],
}


def to_dict(obj: Any) -> dict:
    if obj is None:
        return {}
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


async def get_user_by_name(db: AsyncSession, user_name: str) -> Optional[models.User]:
    result = await db.execute(select(models.User).where(models.User.userName == user_name))
    return result.scalar_one_or_none()


async def get_all(db: AsyncSession, resource: str) -> List[dict]:
    model = RESOURCE_MODELS[resource]
    result = await db.execute(select(model).order_by(model.id))
    return [to_dict(row) for row in result.scalars().all()]


async def get_page(db: AsyncSession, resource: str, page_num: int = 1, page_size: int = 10, keyword: str = "", filters: Optional[Dict[str, Any]] = None) -> dict:
    model = RESOURCE_MODELS[resource]
    query = select(model)
    count_query = select(func.count()).select_from(model)

    for key, value in (filters or {}).items():
        column = getattr(model, key, None)
        if column is not None and value not in (None, ""):
            query = query.where(column == value)
            count_query = count_query.where(column == value)

    if keyword:
        conditions = []
        for field in SEARCHABLE.get(resource, []):
            column = getattr(model, field, None)
            if column is not None:
                conditions.append(column.like(f"%{keyword}%"))
        if conditions:
            query = query.where(or_(*conditions))
            count_query = count_query.where(or_(*conditions))

    total = (await db.execute(count_query)).scalar() or 0
    result = await db.execute(query.order_by(model.id).offset((page_num - 1) * page_size).limit(page_size))
    return {"list": [to_dict(row) for row in result.scalars().all()], "total": total, "pageNum": page_num, "pageSize": page_size}


async def get_by_id(db: AsyncSession, resource: str, item_id: int) -> Optional[dict]:
    model = RESOURCE_MODELS[resource]
    result = await db.execute(select(model).where(model.id == item_id))
    row = result.scalar_one_or_none()
    return to_dict(row) if row else None


async def create(db: AsyncSession, resource: str, payload: dict) -> dict:
    model = RESOURCE_MODELS[resource]
    data = {k: v for k, v in payload.items() if hasattr(model, k) and k != "id"}
    if resource == "users":
        from .security import hash_password

        data["passwordHash"] = hash_password(payload.get("password") or "123456")
    obj = model(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return to_dict(obj)


async def update(db: AsyncSession, resource: str, item_id: int, payload: dict) -> Optional[dict]:
    model = RESOURCE_MODELS[resource]
    result = await db.execute(select(model).where(model.id == item_id))
    obj = result.scalar_one_or_none()
    if not obj:
        return None
    for key, value in payload.items():
        if hasattr(obj, key) and key not in ("id", "passwordHash"):
            setattr(obj, key, value)
    if resource == "users" and payload.get("password"):
        from .security import hash_password

        obj.passwordHash = hash_password(payload["password"])
    await db.commit()
    await db.refresh(obj)
    return to_dict(obj)


async def remove(db: AsyncSession, resource: str, item_id: int) -> bool:
    model = RESOURCE_MODELS[resource]
    result = await db.execute(select(model).where(model.id == item_id))
    obj = result.scalar_one_or_none()
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True


async def get_setting(db: AsyncSession, user_id: int) -> dict:
    result = await db.execute(select(models.UserSetting).where(models.UserSetting.userId == user_id))
    row = result.scalar_one_or_none()
    return row.settings if row and row.settings else {}


async def save_setting(db: AsyncSession, user_id: int, settings: dict) -> dict:
    result = await db.execute(select(models.UserSetting).where(models.UserSetting.userId == user_id))
    row = result.scalar_one_or_none()
    if row:
        row.settings = settings
    else:
        db.add(models.UserSetting(userId=user_id, settings=settings))
    await db.commit()
    return settings
