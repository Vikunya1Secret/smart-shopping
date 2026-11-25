from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.db import Base


def now() -> datetime:
    return datetime.now(timezone.utc)


class Product(Base):
    """Товар. У одного товара может быть несколько предложений (Offer)."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    category: Mapped[str] = mapped_column(String(100))
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    characteristics: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)

    offers: Mapped[list["Offer"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )


class Offer(Base):
    """Предложение: цена товара на конкретном маркетплейсе."""

    __tablename__ = "offers"
    __table_args__ = (UniqueConstraint("product_id", "marketplace"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    marketplace: Mapped[str] = mapped_column(String(50))  # "Wildberries" или "Ozon"
    price: Mapped[int] = mapped_column(Integer)  # цена в рублях
    product_url: Mapped[str] = mapped_column(String(500))
    is_test: Mapped[bool] = mapped_column(Boolean, default=True)  # тестовые данные
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    last_checked_at: Mapped[datetime] = mapped_column(DateTime, default=now)

    product: Mapped["Product"] = relationship(back_populates="offers")