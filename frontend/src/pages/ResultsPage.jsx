import { useEffect, useState } from "react";
import { searchProducts } from "../services/api.js";
import SearchBar from "../components/SearchBar.jsx";
import Filters from "../components/Filters.jsx";
import ProductCard from "../components/ProductCard.jsx";
import GroupBlock from "../components/GroupBlock.jsx";

// Собирает предложения в группы по group_id, сохраняя порядок
function groupItems(items) {
  const groups = new Map();
  for (const item of items) {
    if (!groups.has(item.group_id)) groups.set(item.group_id, []);
    groups.get(item.group_id).push(item);
  }
  return [...groups.values()];
}

export default function ResultsPage({ query, onSearch, onHome }) {
  const [marketplace, setMarketplace] = useState("");
  const [sort, setSort] = useState("relevance");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Запрос к backend при смене запроса, фильтра или сортировки
  useEffect(() => {
    let cancelled = false; // защита от устаревшего ответа
    setLoading(true);
    setError("");

    searchProducts(query, marketplace, sort)
      .then((result) => {
        if (!cancelled) setData(result);
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err.message);
          setData(null);
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [query, marketplace, sort]);

  function renderResults() {
    if (loading) return <p className="status">Загрузка…</p>;
    if (error) return <p className="status error">{error}</p>;
    if (!data || data.total === 0) {
      return <p className="status">По запросу «{query}» ничего не найдено.</p>;
    }

    // Режим «с группировкой»: похожие предложения показываем вместе
    if (sort === "relevance") {
      return (
        <div className="grid">
          {groupItems(data.items).map((group) =>
            group.length > 1 ? (
              <GroupBlock key={group[0].group_id} items={group} />
            ) : (
              <ProductCard key={group[0].offer_id} item={group[0]} />
            )
          )}
        </div>
      );
    }

    // Режим сортировки по цене: обычный список карточек
    return (
      <div className="grid">
        {data.items.map((item) => (
          <ProductCard key={item.offer_id} item={item} />
        ))}
      </div>
    );
  }

  return (
    <>
      <header className="topbar">
        <button className="logo" onClick={onHome}>Сравнение цен</button>
        <div className="topbar-search">
          <SearchBar initialValue={query} onSearch={onSearch} />
        </div>
      </header>

      <main className="results">
        <div className="results-head">
          <h1>Результаты по запросу «{query}»</h1>
          {data && !loading && <p>Найдено предложений: {data.total}</p>}
        </div>

        <Filters
          marketplace={marketplace}
          sort={sort}
          onMarketplaceChange={setMarketplace}
          onSortChange={setSort}
        />

        <p className="demo-note">
          Данные тестовые: цены придуманы, а ссылки ведут на страницу поиска маркетплейса.
        </p>

        {renderResults()}
      </main>
    </>
  );
}