export default function Filters({ marketplace, sort, onMarketplaceChange, onSortChange }) {
  return (
    <div className="filters">
      <label>
        Маркетплейс
        <select value={marketplace} onChange={(e) => onMarketplaceChange(e.target.value)}>
          <option value="">Все</option>
          <option value="Wildberries">Wildberries</option>
          <option value="Ozon">Ozon</option>
        </select>
      </label>

      <label>
        Сортировка
        <select value={sort} onChange={(e) => onSortChange(e.target.value)}>
          <option value="relevance">С группировкой похожих</option>
          <option value="price_asc">Сначала дешёвые</option>
          <option value="price_desc">Сначала дорогие</option>
        </select>
      </label>
    </div>
  );
}