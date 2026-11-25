from pathlib import Path

# Папка backend/ (на два уровня выше этого файла)
BASE_DIR = Path(__file__).resolve().parent.parent

# Файл базы данных SQLite появится в папке backend/
DATABASE_URL = f"sqlite:///{BASE_DIR / 'products.db'}"

# Адреса, с которых frontend (Vite) может обращаться к API
FRONTEND_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]