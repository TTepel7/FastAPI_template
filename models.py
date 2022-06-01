from sqlalchemy import Numeric, Table, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

# Вспомогательная таблица для связи многие ко многим у категорий и продуктов
product_category = Table('product_category', Base.metadata,
                         Column('product_id', ForeignKey('products.id'), primary_key=True),
                         Column('category_id', ForeignKey('categories.id'), primary_key=True)
                         )


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255), nullable=True)
    # Если использовать backref то необезательно указывать связи в обеих таблицах
    # products = relationship('Product', secondary="product_category", back_populates='categories')


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255), nullable=True)
    price = Column(Numeric, default=0)

    # backref автоматически делает связь в другой таблице
    categories = relationship("Category", secondary="product_category", backref="products")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
