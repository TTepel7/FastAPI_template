from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd

router = APIRouter(
    prefix="/category",
    tags=["category"],
)


# получение всех категорий
@router.get("/", response_model=List[pyd.CategorySchema])
async def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()


# получение категории по id
@router.get("/{category_id}")
async def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    q = db.query(models.Category).filter(models.Category.id == category_id).first()
    if q:
        return q
    raise HTTPException(status_code=404, detail="Category not found")


# получение категории по id
@router.post("/", response_model=pyd.CategorySchema)
async def create_category(category_input: pyd.CategoryCreate, db: Session = Depends(get_db)):
    # автозаполнение  всех полей
    cat_db = models.Category(
        **category_input.dict()
    )
    db.add(cat_db)
    db.commit()
    return cat_db
