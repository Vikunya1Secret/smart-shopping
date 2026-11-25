from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from config import FRONTEND_ORIGINS
from backend.app.database.db import init_db
from backend.app.routes import products


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Выполняется один раз при запуске сервера
    init_db()
    yield


app = FastAPI(title="Сравнение товаров", lifespan=lifespan)

# CORS разрешает браузеру на странице React обращаться к этому API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)