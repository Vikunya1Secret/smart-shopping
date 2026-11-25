import re

STOP_WORDS = {"для", "и", "с", "в", "на", "по"}


def normalize(text: str) -> str:
    """Нижний регистр, «ё» -> «е»."""
    return text.lower().replace("ё", "е")


def split_words(text: str) -> list[str]:
    """Разбивает текст на слова из букв и цифр: 'WH-1000XM5' -> ['wh', '1000xm5']."""
    return re.findall(r"[a-zа-я0-9]+", normalize(text))


def tokenize(name: str) -> set[str]:
    return {w for w in split_words(name) if w not in STOP_WORDS}


def model_codes(tokens: set[str]) -> set[str]:
    """Слова с цифрами (g435, 1000xm5, 128) считаем кодами модели."""
    return {w for w in tokens if any(ch.isdigit() for ch in w)}


def names_similar(a: str, b: str, threshold: float = 0.5) -> bool:
    """Похожи ли названия: одинаковые коды модели и достаточно общих слов."""
    ta, tb = tokenize(a), tokenize(b)
    if not ta or not tb:
        return False
    if model_codes(ta) != model_codes(tb):
        return False
    return len(ta & tb) / len(ta | tb) >= threshold


def group_products(products) -> dict[int, int]:
    """Возвращает {product_id: group_id}. Похожие товары одной категории
    получают общий group_id (наименьший id в группе)."""
    parent = {p.id: p.id for p in products}

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, a in enumerate(products):
        for b in products[i + 1:]:
            if a.category == b.category and names_similar(a.name, b.name):
                ra, rb = find(a.id), find(b.id)
                if ra != rb:
                    parent[max(ra, rb)] = min(ra, rb)

    return {p.id: find(p.id) for p in products}