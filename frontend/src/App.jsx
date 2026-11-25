import { useState } from "react";
import HomePage from "./pages/HomePage.jsx";
import ResultsPage from "./pages/ResultsPage.jsx";

export default function App() {
  // null = мы на главной, строка = текущий поисковый запрос
  const [query, setQuery] = useState(null);

  if (query === null) {
    return <HomePage onSearch={setQuery} />;
  }
  return (
    <ResultsPage
      query={query}
      onSearch={setQuery}
      onHome={() => setQuery(null)}
    />
  );
}