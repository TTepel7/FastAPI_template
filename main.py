from fastapi import FastAPI
import models
from database import SessionLocal, engine
from routers import category_router, product_router, user_router

# создание таблиц в БД из моделей
models.Base.metadata.create_all(bind=engine)

# Инициализация фастапи
app = FastAPI()

# подключение АпиРоутера (маршруты сущности)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
