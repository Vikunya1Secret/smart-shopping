from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from backend.app.database.db import get_db
from backend.app.database.models import Product
from backend.app.schemas import ProductOut, SearchResponse
from backend.app.services.search import search_offers

router = APIRouter(prefix="/api")


@router.get("/health")
def health():
    """Проверка, что backend запущен."""
    return {"status": "ok"}


@router.get("/search", response_model=SearchResponse)
def search(
    q: str = "",
    marketplace: Literal["Wildberries", "Ozon"] | None = None,
    sort: Literal["relevance", "price_asc", "price_desc"] = "relevance",
    db: Session = Depends(get_db),
):
    """Поиск предложений по названию. Можно фильтровать по маркетплейсу и сортировать по цене."""
    query = q.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Введите поисковый запрос")

    items = search_offers(db, query, marketplace, sort)
    return SearchResponse(query=query, total=len(items), items=items)


@router.get("/products", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    """Все сохранённые товары вместе с предложениями."""
    stmt = select(Product).options(selectinload(Product.offers)).order_by(Product.name)
    return db.scalars(stmt).all()


@router.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Один товар по id."""
    stmt = select(Product).options(selectinload(Product.offers)).where(Product.id == product_id)
    product = db.scalar(stmt)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product