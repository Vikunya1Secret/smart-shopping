import { useState } from "react";

export default function SearchBar({ initialValue = "", onSearch }) {
  const [value, setValue] = useState(initialValue);
  const [error, setError] = useState("");

  function handleSubmit(event) {
    event.preventDefault(); // не перезагружать страницу
    const text = value.trim();
    if (!text) {
      setError("Введите название товара");
      return;
    }
    setError("");
    onSearch(text);
  }

  return (
    <div>
      <form className="search-bar" onSubmit={handleSubmit}>
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Например: наушники Sony"
          aria-label="Поиск товара"
        />
        <button type="submit">Найти</button>
      </form>
      {error && <p className="field-error">{error}</p>}
    </div>
  );
}