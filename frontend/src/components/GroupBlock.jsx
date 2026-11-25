import ProductCard from "./ProductCard.jsx";

export default function GroupBlock({ items }) {
  const prices = items.map((i) => i.price);
  const difference = Math.max(...prices) - Math.min(...prices);

  return (
    <section className="group">
      <div className="group-header">
        <h2>Сравнение предложений</h2>
        <p>
          {items.length} предложения
          {difference > 0
            ? `, разница в цене: ${difference.toLocaleString("ru-RU")} ₽`
            : ", цены одинаковые"}
        </p>
      </div>
      <div className="grid">
        {items.map((item) => (
          <ProductCard key={item.offer_id} item={item} />
        ))}
      </div>
    </section>
  );
}