import { useState } from "react";

function formatPrice(price) {
  return price.toLocaleString("ru-RU") + " ₽";
}

export default function ProductCard({ item }) {
  // Если картинки нет или она не загрузилась, показываем заглушку
  const [imageFailed, setImageFailed] = useState(false);
  const showImage = item.image_url && !imageFailed;

  const marketplaceClass = item.marketplace === "Wildberries" ? "badge wb" : "badge ozon";

  return (
    <article className="card">
      <div className="card-image">
        {showImage ? (
          <img
            src={item.image_url}
            alt={item.name}
            loading="lazy"
            onError={() => setImageFailed(true)}
          />
        ) : (
          <div className="image-placeholder">Нет фото</div>
        )}
        {item.is_best_price && <span className="best-price">Лучшая цена</span>}
      </div>

      <div className="card-body">
        <div className="badges">
          <span className={marketplaceClass}>{item.marketplace}</span>
          {item.is_test && <span className="badge test">Тестовые данные</span>}
        </div>

        <h3 className="card-title">{item.name}</h3>
        {item.characteristics && <p className="card-specs">{item.characteristics}</p>}

        <div className="card-price">{formatPrice(item.price)}</div>

        <a
          className="btn"
          href={item.product_url}
          target="_blank"
          rel="noopener noreferrer"
        >
          Перейти к товару
        </a>
      </div>
    </article>
  );
}