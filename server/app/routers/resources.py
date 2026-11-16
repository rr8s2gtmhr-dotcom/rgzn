from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud
from ..database import get_db
from ..schemas import ApiResponse, PageResult
from ..security import get_current_user

router = APIRouter(prefix="/api", tags=["业务数据"])


@router.get("/{resource}/page", response_model=ApiResponse[PageResult[dict]])
async def page_resource(
    resource: str,
    pageNum: int = 1,
    pageSize: int = 10,
    keyword: str = "",
    unitId: int | None = None,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    if resource not in crud.RESOURCE_MODELS:
        raise HTTPException(status_code=404, detail="未知资源")
    filters = {"unitId": unitId}
    result = await crud.get_page(db, resource, pageNum, pageSize, keyword, filters)
    return ApiResponse(data=result)


@router.get("/{resource}", response_model=ApiResponse[list])
async def list_resource(resource: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    if resource not in crud.RESOURCE_MODELS:
        raise HTTPException(status_code=404, detail="未知资源")
    return ApiResponse(data=await crud.get_all(db, resource))


@router.get("/{resource}/{item_id}", response_model=ApiResponse[dict])
async def get_resource(resource: str, item_id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    if resource not in crud.RESOURCE_MODELS:
        raise HTTPException(status_code=404, detail="未知资源")
    row = await crud.get_by_id(db, resource, item_id)
    if not row:
        raise HTTPException(status_code=404, detail="记录不存在")
    return ApiResponse(data=row)


@router.post("/{resource}", response_model=ApiResponse[dict])
async def create_resource(resource: str, payload: dict, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    if resource not in crud.RESOURCE_MODELS:
        raise HTTPException(status_code=404, detail="未知资源")
    return ApiResponse(data=await crud.create(db, resource, payload))


@router.put("/{resource}/{item_id}", response_model=ApiResponse[dict])
async def update_resource(resource: str, item_id: int, payload: dict, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    if resource not in crud.RESOURCE_MODELS:
        raise HTTPException(status_code=404, detail="未知资源")
    row = await crud.update(db, resource, item_id, payload)
    if not row:
        raise HTTPException(status_code=404, detail="记录不存在")
    return ApiResponse(data=row)


@router.delete("/{resource}/{item_id}", response_model=ApiResponse)
async def delete_resource(resource: str, item_id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    if resource not in crud.RESOURCE_MODELS:
        raise HTTPException(status_code=404, detail="未知资源")
    if not await crud.remove(db, resource, item_id):
        raise HTTPException(status_code=404, detail="记录不存在")
    return ApiResponse(message="删除成功")
