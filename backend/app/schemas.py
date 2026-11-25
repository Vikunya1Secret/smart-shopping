from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OfferOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    marketplace: str
    price: int
    product_url: str
    is_test: bool
    updated_at: datetime
    last_checked_at: datetime


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    image_url: str | None
    characteristics: str | None
    created_at: datetime
    offers: list[OfferOut]


class SearchItem(BaseModel):
    """Одна карточка в результатах поиска = одно предложение."""

    offer_id: int
    product_id: int
    group_id: int          # одинаковый у похожих товаров (для сравнения)
    name: str
    category: str
    image_url: str | None
    characteristics: str | None
    marketplace: str
    price: int
    product_url: str
    is_test: bool
    is_best_price: bool    # самая низкая цена среди предложений своей группы


class SearchResponse(BaseModel):
    query: str
    total: int
    items: list[SearchItem]