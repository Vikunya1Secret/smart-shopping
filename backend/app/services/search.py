from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from backend.app.database.models import Product
from backend.app.schemas import SearchItem
from backend.app.services.matching import group_products, normalize, split_words


def search_offers(
    db: Session,
    query: str,
    marketplace: str | None = None,
    sort: str = "relevance",
) -> list[SearchItem]:
    words = split_words(query)
    if not words:
        return []

    products = db.scalars(select(Product).options(selectinload(Product.offers))).all()

    matched = []
    for p in products:
        haystack = normalize(f"{p.name} {p.category}")
        if all(w in haystack for w in words):
            matched.append(p)

    groups = group_products(matched)

    min_price: dict[int, int] = {}
    offers_count: dict[int, int] = {}
    for p in matched:
        g = groups[p.id]
        for o in p.offers:
            min_price[g] = min(min_price.get(g, o.price), o.price)
            offers_count[g] = offers_count.get(g, 0) + 1

    items = []
    for p in matched:
        g = groups[p.id]
        for o in p.offers:
            items.append(
                SearchItem(
                    offer_id=o.id,
                    product_id=p.id,
                    group_id=g,
                    name=p.name,
                    category=p.category,
                    image_url=p.image_url,
                    characteristics=p.characteristics,
                    marketplace=o.marketplace,
                    price=o.price,
                    product_url=o.product_url,
                    is_test=o.is_test,
                    is_best_price=offers_count[g] > 1 and o.price == min_price[g],
                )
            )

    if marketplace:
        items = [i for i in items if i.marketplace == marketplace]

    if sort == "price_asc":
        items.sort(key=lambda i: i.price)
    elif sort == "price_desc":
        items.sort(key=lambda i: i.price, reverse=True)
    else:
        items.sort(key=lambda i: (i.group_id, i.price))

    return items