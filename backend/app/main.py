from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import (
    engine,
    Base,
    get_db
)

from app.models import (
    Product,
    Customer,
    Order,
    OrderItem
)

from app.schemas import (
    ProductCreate,
    ProductUpdate,
    CustomerCreate,
    CustomerUpdate,
    OrderCreate
)

app = FastAPI(
    title="Inventory Management System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

####################################################
# PRODUCT APIs
####################################################


@app.post("/products")
def create_product(
        product: ProductCreate,
        db: Session = Depends(get_db)
):

    existing = db.query(Product).filter(
        Product.sku == product.sku
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="SKU already exists"
        )

    db_product = Product(**product.dict())

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


@app.get("/products")
def get_products(
        db: Session = Depends(get_db)
):
    return db.query(Product).all()


@app.get("/products/{product_id}")
def get_product(
        product_id: int,
        db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            404,
            "Product not found"
        )

    return product


@app.put("/products/{product_id}")
def update_product(
        product_id: int,
        payload: ProductUpdate,
        db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            404,
            "Product not found"
        )

    product.name = payload.name
    product.sku = payload.sku
    product.price = payload.price
    product.stock = payload.stock

    db.commit()

    return product


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    order_item = db.query(OrderItem).filter(
        OrderItem.product_id == product_id
    ).first()

    if order_item:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete product. Product is used in orders."
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }


####################################################
# CUSTOMER APIs
####################################################

@app.post("/customers")
def create_customer(
        customer: CustomerCreate,
        db: Session = Depends(get_db)
):

    existing = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing:
        raise HTTPException(
            400,
            "Email already exists"
        )

    db_customer = Customer(**customer.dict())

    db.add(db_customer)

    db.commit()

    db.refresh(db_customer)

    return db_customer


@app.get("/customers")
def get_customers(
        db: Session = Depends(get_db)
):
    return db.query(Customer).all()


@app.get("/customers/{customer_id}")
def get_customer(
        customer_id: int,
        db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            404,
            "Customer not found"
        )

    return customer


@app.put("/customers/{customer_id}")
def update_customer(
        customer_id: int,
        payload: CustomerUpdate,
        db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            404,
            "Customer not found"
        )

    customer.name = payload.name
    customer.email = payload.email

    db.commit()

    return customer


@app.delete("/customers/{customer_id}")
def delete_customer(
        customer_id: int,
        db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            404,
            "Customer not found"
        )

    db.delete(customer)

    db.commit()

    return {"message": "Deleted successfully"}


####################################################
# ORDER APIs
####################################################

@app.post("/orders")
def create_order(
        order_data: OrderCreate,
        db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == order_data.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            404,
            "Customer not found"
        )

    total_amount = 0

    products_to_update = []

    for item in order_data.items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if not product:
            raise HTTPException(
                404,
                f"Product {item.product_id} not found"
            )

        if product.stock < item.quantity:
            raise HTTPException(
                400,
                f"Insufficient stock for {product.name}"
            )

        total_amount += (
            product.price * item.quantity
        )

        products_to_update.append(
            (product, item.quantity)
        )

    order = Order(
        customer_id=order_data.customer_id,
        total_amount=total_amount
    )

    db.add(order)

    db.flush()

    for item in order_data.items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )

        db.add(order_item)

    for product, qty in products_to_update:
        product.stock -= qty

    db.commit()

    return {
        "message": "Order Created",
        "order_id": order.id,
        "total_amount": total_amount
    }


@app.get("/orders")
def get_orders(
        db: Session = Depends(get_db)
):

    orders = db.query(Order).all()

    response = []

    for order in orders:

        response.append({
            "id": order.id,
            "customer_id": order.customer_id,
            "total_amount": order.total_amount,
            "created_at": order.created_at
        })

    return response


@app.get("/orders/{order_id}")
def get_order(
        order_id: int,
        db: Session = Depends(get_db)
):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            404,
            "Order not found"
        )

    items = []

    for item in order.items:

        items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item.price
        })

    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "total_amount": order.total_amount,
        "created_at": order.created_at,
        "items": items
    }