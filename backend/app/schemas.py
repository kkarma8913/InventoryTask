# app/schemas.py

from pydantic import BaseModel
from typing import List


# Product

class ProductCreate(BaseModel):
    name: str
    sku: str
    price: float
    stock: int


class ProductUpdate(BaseModel):
    name: str
    sku: str
    price: float
    stock: int


# Customer

class CustomerCreate(BaseModel):
    name: str
    email: str


class CustomerUpdate(BaseModel):
    name: str
    email: str


# Order

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]