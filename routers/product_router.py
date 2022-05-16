from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd

router = APIRouter(
    prefix="/product",
    tags=["product"],
)


# получение всех продуктов
@router.get("/", response_model=List[pyd.ProductSchema])
async def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


# получение категории по id
@router.get("/{product_id}")
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    q = db.query(models.Product).filter(models.Product.id == product_id).first()
    if q:
        return q
    raise HTTPException(status_code=404, detail="Product not found")


# получение категории по id
@router.post("/", response_model=pyd.ProductSchema)
async def create_product(product_input: pyd.ProductCreate, db: Session = Depends(get_db)):
    # создание продукта
    prod_db = models.Product()
    prod_db.name = product_input.name
    prod_db.description = product_input.description
    prod_db.price = product_input.price

    # пройтись по циклу с id категорий, искать их в БД, если есть добавить, иначе ошибка
    for cat_id in product_input.category_ids:
        cat_db = db.query(models.Category).filter(models.Category.id == cat_id).first()
        if cat_db:
            prod_db.categories.append(cat_db)
        else:
            raise HTTPException(status_code=404, detail="Category not found")

    db.add(prod_db)
    db.commit()
    return prod_db
