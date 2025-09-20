from pydantic import BaseModel

class ItemCreate(BaseModel):

    title: str
    description: str
    price: int
    in_stock: int | None

class ItemRead(BaseModel):

    id: int
    title: str
    description: str
    price: int
    in_stock: int | None

    class Config:
        from_attributes = True