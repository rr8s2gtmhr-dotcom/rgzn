from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud
from ..database import get_db
from ..schemas import ApiResponse, SettingRequest
from ..security import get_current_user

router = APIRouter(prefix="/api/settings", tags=["用户设置"])


@router.get("/theme", response_model=ApiResponse[dict])
async def get_theme(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    settings = await crud.get_setting(db, current_user.id)
    return ApiResponse(data=settings)


@router.put("/theme", response_model=ApiResponse[dict])
async def save_theme(payload: SettingRequest, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    settings = await crud.save_setting(db, current_user.id, payload.settings)
    return ApiResponse(data=settings)
