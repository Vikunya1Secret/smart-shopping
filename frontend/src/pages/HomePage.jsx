import SearchBar from "../components/SearchBar.jsx";

const EXAMPLES = ["наушники", "смартфон", "клавиатура Logitech", "монитор LG"];

export default function HomePage({ onSearch }) {
  return (
    <main className="home">
      <h1>Сравнение цен</h1>
      <p className="subtitle">
        Ищите товар и сравнивайте предложения Wildberries и Ozon на одной странице,
        чтобы выбрать самую выгодную цену.
      </p>

      <div className="home-search">
        <SearchBar onSearch={onSearch} />
      </div>

      <div className="examples">
        <span>Попробуйте:</span>
        {EXAMPLES.map((text) => (
          <button key={text} className="chip" onClick={() => onSearch(text)}>
            {text}
          </button>
        ))}
      </div>

      <div className="marketplaces">
        <span className="badge wb">Wildberries</span>
        <span className="badge ozon">Ozon</span>
      </div>

      <p className="demo-note">
        Учебный проект: используются тестовые данные, цены и ссылки не настоящие.
      </p>
    </main>
  );
}