export async function searchProducts(q, marketplace, sort) {
  const params = new URLSearchParams({ q, sort });
  if (marketplace) params.set("marketplace", marketplace);

  let response;
  try {
    response = await fetch(`/api/search?${params}`);
  } catch {
    throw new Error("Не удалось связаться с сервером. Проверьте, что backend запущен.");
  }

  if (!response.ok) {
    const data = await response.json().catch(() => null);
    const message = typeof data?.detail === "string" ? data.detail : "Ошибка сервера";
    throw new Error(message);
  }
  return response.json();
}