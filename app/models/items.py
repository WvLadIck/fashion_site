from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseModel

class Items(BaseModel):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(256))
    price: Mapped[float] = mapped_column(Float)
    in_stock: Mapped[int] = mapped_column(Integer)