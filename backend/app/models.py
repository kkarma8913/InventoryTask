# app/models.py

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    sku = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    price = Column(Float, nullable=False)

    stock = Column(Integer, default=0)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )

    total_amount = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    customer = relationship("Customer")

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    quantity = Column(Integer)

    price = Column(Float)

    order = relationship(
        "Order",
        back_populates="items"
    )

    product = relationship("Product")