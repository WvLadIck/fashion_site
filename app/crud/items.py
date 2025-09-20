from sqlalchemy.ext.asyncio import AsyncSession

from app.models.items import Items
from app.schemas.items import ItemCreate, ItemRead


async def create(session: AsyncSession, data: ItemCreate):
    item = Items(**data.model_dump())
    session.add(item)
    await session.commit()
    await session.refresh(item)

    return ItemRead.model_validate(item)
