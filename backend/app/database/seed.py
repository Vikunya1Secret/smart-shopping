from urllib.parse import quote, quote_plus

from sqlalchemy import func, select

from backend.app.database.db import SessionLocal, init_db
from backend.app.database.models import Offer, Product, now

WB = "Wildberries"
OZON = "Ozon"

SEARCH_URLS = {
    WB: "https://www.wildberries.ru/catalog/0/search.aspx?search={}",
    OZON: "https://www.ozon.ru/search/?text={}",
}


def img(text: str) -> str:
    """Картинка-заглушка с подписью (сервис placehold.co)."""
    return "https://placehold.co/400x400/png?text=" + quote_plus(text)


TEST_PRODUCTS = [
    # --- Электроника ---
    ("Sony WH-1000XM5 наушники беспроводные", "Электроника", img("Sony WH-1000XM5"),
     "Bluetooth 5.2; шумоподавление; до 30 часов работы", {WB: 27990, OZON: 28490}),
    ("Samsung Galaxy S24 смартфон 128 ГБ", "Электроника", img("Samsung Galaxy S24"),
     "Экран 6.2 дюйма; 128 ГБ памяти; 8 ГБ ОЗУ", {WB: 64990, OZON: 62990}),
    ("Apple AirPods Pro 2 наушники", "Электроника", img("AirPods Pro 2"),
     "Bluetooth 5.3; активное шумоподавление; кейс MagSafe", {WB: 21990, OZON: 22490}),
    ("Xiaomi Redmi Note 13 смартфон 128 ГБ", "Электроника", img("Redmi Note 13"),
     "AMOLED 6.67 дюйма; 128 ГБ памяти; камера 108 Мп", {WB: 18490, OZON: 17990}),
    ("JBL Charge 5 портативная колонка", "Электроника", img("JBL Charge 5"),
     "Защита IP67; до 20 часов работы; функция Powerbank", {WB: 11990}),


    ("Наушники Logitech G435 игровые беспроводные", "Компьютерная техника", img("Logitech G435"),
     "Lightspeed и Bluetooth; вес 165 г; до 18 часов работы", {WB: 4990}),
    ("Logitech G435 Lightspeed наушники игровые", "Компьютерная техника", img("Logitech G435"),
     "Lightspeed и Bluetooth; вес 165 г; до 18 часов работы", {OZON: 5290}),
    ("ASUS Vivobook 15 X1504ZA ноутбук", "Компьютерная техника", img("ASUS Vivobook 15"),
     "15.6 дюйма; Core i5; 16 ГБ ОЗУ; SSD 512 ГБ", {WB: 46990, OZON: 45490}),
    ("Logitech K380 клавиатура беспроводная", "Компьютерная техника", img("Logitech K380"),
     "Bluetooth; тихие клавиши; подключение до 3 устройств", {WB: 3990, OZON: 3790}),
    ("Logitech MX Master 3S мышь беспроводная", "Компьютерная техника", img("MX Master 3S"),
     "8000 DPI; тихие клики; зарядка USB-C", {WB: 8990, OZON: 9290}),
    ("Монитор LG UltraGear 27GP850-B 27 дюймов", "Компьютерная техника", img("LG 27GP850-B"),
     "IPS; 2560x1440; 165 Гц; отклик 1 мс", {WB: 32990}),
    ("LG UltraGear 27GP850-B монитор игровой 27 дюймов", "Компьютерная техника", img("LG 27GP850-B"),
     "IPS; 2560x1440; 165 Гц; отклик 1 мс", {OZON: 31990}),
    ("Samsung 970 EVO Plus SSD 1 ТБ", "Компьютерная техника", img("Samsung 970 EVO Plus"),
     "M.2 NVMe; чтение до 3500 МБ/с; 1 ТБ", {OZON: 8290}),

    ("Робот-пылесос Xiaomi Robot Vacuum S10", "Бытовая техника", img("Xiaomi Vacuum S10"),
     "Влажная и сухая уборка; лазерная навигация; до 130 минут", {WB: 19990, OZON: 18990}),
    ("Электрочайник Bosch TWK3A011", "Бытовая техника", img("Bosch TWK3A011"),
     "Объём 1.7 л; мощность 2400 Вт; пластиковый корпус", {WB: 2990, OZON: 3190}),
    ("Блендер Braun MQ 5200 погружной", "Бытовая техника", img("Braun MQ 5200"),
     "Мощность 1000 Вт; 2 скорости; насадка-венчик", {WB: 5490, OZON: 5290}),

    ("Внешний аккумулятор Xiaomi Power Bank 20000 мАч", "Аксессуары", img("Xiaomi Power Bank"),
     "20000 мАч; быстрая зарядка 22.5 Вт; USB-C", {WB: 2490, OZON: 2390}),
    ("Чехол для iPhone 15 силиконовый", "Аксессуары", img("iPhone 15 case"),
     "Силикон; мягкая подкладка; несколько цветов", {WB: 1290}),
    ("Кабель USB-C Anker PowerLine III 1.8 м", "Аксессуары", None,
     "Длина 1.8 м; зарядка до 60 Вт; нейлоновая оплётка", {OZON: 990}),
]


def seed() -> None:
    init_db()
    db = SessionLocal()
    added_products = 0
    added_offers = 0
    try:
        for name, category, image_url, characteristics, prices in TEST_PRODUCTS:
            product = db.scalar(select(Product).where(Product.name == name))
            if product is None:
                product = Product(
                    name=name,
                    category=category,
                    image_url=image_url,
                    characteristics=characteristics,
                )
                db.add(product)
                db.flush()
                added_products += 1

            for marketplace, price in prices.items():
                url = SEARCH_URLS[marketplace].format(quote(name))
                offer = db.scalar(
                    select(Offer).where(
                        Offer.product_id == product.id,
                        Offer.marketplace == marketplace,
                    )
                )
                if offer is None:
                    db.add(Offer(product_id=product.id, marketplace=marketplace,
                                 price=price, product_url=url, is_test=True))
                    added_offers += 1
                elif offer.price != price or offer.product_url != url:
                    offer.price = price
                    offer.product_url = url
                    offer.updated_at = now()

        db.commit()

        total_products = db.scalar(select(func.count()).select_from(Product))
        total_offers = db.scalar(select(func.count()).select_from(Offer))
        print(f"Добавлено: товаров {added_products}, предложений {added_offers}")
        print(f"Всего в базе: товаров {total_products}, предложений {total_offers}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()