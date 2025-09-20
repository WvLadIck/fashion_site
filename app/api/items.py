from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.db.base import get_db
from app.schemas.items import ItemCreate, ItemRead

router = APIRouter()

@router.post("/add_item", response_model=ItemRead)
async def create_item(data: ItemCreate, session: AsyncSession = Depends(get_db)):
    return await crud.items.create(session=session, data=data)
