from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud
from ..database import get_db
from ..schemas import ApiResponse, LoginRequest
from ..security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/login", response_model=ApiResponse[dict])
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_name(db, payload.userName)
    if not user or not verify_password(payload.password, user.passwordHash):
        raise HTTPException(status_code=400, detail="账号或密码错误")
    if not user.status:
        raise HTTPException(status_code=403, detail="账号已被禁用")

    roles = []
    btn_permissions = []
    menu_paths = []
    from sqlalchemy import select
    for role_id in user.roleIds or []:
        result = await db.execute(select(crud.models.Role).where(crud.models.Role.id == role_id))
        role = result.scalar_one_or_none()
        if role:
            roles.append(role.code)
            btn_permissions.extend(role.btnPermissions or [])
            menu_paths.extend(role.menuPaths or [])

    token = create_access_token({"sub": user.userName})
    data = {
        "token": token,
        "userName": user.userName,
        "roles": roles,
        "authBtnList": list(dict.fromkeys(btn_permissions)),
        "menuPaths": list(dict.fromkeys(menu_paths)),
        "userInfos": {
            "userName": user.userName,
            "realName": user.realName,
            "photo": "",
            "roles": roles,
            "time": 0,
            "unitId": user.unitId,
            "userId": user.id,
        },
    }
    return ApiResponse(data=data)


@router.get("/me", response_model=ApiResponse[dict])
async def me(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select

    roles = []
    btn_permissions = []
    menu_paths = []
    for role_id in current_user.roleIds or []:
        result = await db.execute(select(crud.models.Role).where(crud.models.Role.id == role_id))
        role = result.scalar_one_or_none()
        if role:
            roles.append(role.code)
            btn_permissions.extend(role.btnPermissions or [])
            menu_paths.extend(role.menuPaths or [])
    return ApiResponse(data={
        "userName": current_user.userName,
        "realName": current_user.realName,
        "photo": "",
        "roles": roles,
        "authBtnList": list(dict.fromkeys(btn_permissions)),
        "menuPaths": list(dict.fromkeys(menu_paths)),
        "time": 0,
        "unitId": current_user.unitId,
        "userId": current_user.id,
    })


@router.post("/logout", response_model=ApiResponse)
async def logout():
    return ApiResponse(message="已退出")
