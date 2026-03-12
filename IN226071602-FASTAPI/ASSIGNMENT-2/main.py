from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# ------------------ Pydantic Models ------------------

class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=100)
    delivery_address: str = Field(..., min_length=10)

class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)

class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: list[OrderItem] = Field(..., min_items=1)

# ------------------ Data ------------------

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationary", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationary", "in_stock": True},
]

orders = []
order_counter = 1
feedback = []

# ------------------ Endpoints ------------------

@app.get("/")
def home():
    return {"message": "Welcome to our E-commerce API"}

@app.get("/products")
def get_all_products():
    return {"products": products, "total": len(products)}

@app.get("/products/filter")
def filter_products(
    min_price: Optional[int] = Query(None),
    max_price: Optional[int] = Query(None),
    category: Optional[str] = Query(None)
):
    filtered_products = products

    if min_price is not None:
        filtered_products = [p for p in filtered_products if p["price"] >= min_price]

    if max_price is not None:
        filtered_products = [p for p in filtered_products if p["price"] <= max_price]

    if category is not None:
        filtered_products = [
            p for p in filtered_products
            if p["category"].lower() == category.lower()
        ]

    return {
        "filters_applied": {
            "min_price": min_price,
            "max_price": max_price,
            "category": category
        },
        "count": len(filtered_products),
        "products": filtered_products
    }

@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    filtered_products = [p for p in products if p["category"].lower() == category_name.lower()]

    if not filtered_products:
        return {"error": "No products found in this category"}

    return {"category": category_name, "products": filtered_products}

@app.get("/products/instock")
def get_instock_products():
    instock_products = [p for p in products if p["in_stock"]]
    return {"in_stock_products": instock_products, "count": len(instock_products)}

@app.get("/store/summary")
def store_summary():
    total_products = len(products)
    in_stock = len([p for p in products if p["in_stock"]])
    out_of_stock = total_products - in_stock
    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock,
        "out_of_stock": out_of_stock,
        "categories": categories
    }

@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    matched_products = [
        p for p in products if keyword.lower() in p["name"].lower()
    ]

    if not matched_products:
        return {"message": "No products matched your search"}

    return {"matched_products": matched_products, "count": len(matched_products)}

@app.get("/products/deals")
def get_product_deals():
    cheapest_product = min(products, key=lambda x: x["price"])
    expensive_product = max(products, key=lambda x: x["price"])

    return {"best_deal": cheapest_product, "premium_pick": expensive_product}

@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        return {"error": "Product not found"}

    return {"name": product["name"], "price": product["price"]}

# ------------------ Feedback ------------------

@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):
    feedback.append(data.dict())

    return {
        "message": "Feedback submitted successfully",
        "feedback": data,
        "total_feedback": len(feedback)
    }

# ------------------ Product Summary ------------------

@app.get("/products/summary")
def products_summary():
    total_products = len(products)
    in_stock_count = len([p for p in products if p["in_stock"]])
    out_of_stock_count = total_products - in_stock_count

    cheapest_product = min(products, key=lambda x: x["price"])
    most_expensive_product = max(products, key=lambda x: x["price"])

    categories = list(set([p["category"] for p in products]))

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "most_expensive": {
            "name": most_expensive_product["name"],
            "price": most_expensive_product["price"]
        },
        "cheapest": {
            "name": cheapest_product["name"],
            "price": cheapest_product["price"]
        },
        "categories": categories
    }

# ------------------ Bulk Orders ------------------

@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):

    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:

        product = next((p for p in products if p["id"] == item.product_id), None)

        if not product:
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })
            continue

        if not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f"{product['name']} is out of stock"
            })
            continue

        subtotal = product["price"] * item.quantity
        grand_total += subtotal

        confirmed.append({
            "product": product["name"],
            "qty": item.quantity,
            "subtotal": subtotal
        })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }

# ------------------ Order Status Tracker ------------------

@app.post("/orders")
def create_order(order: OrderRequest):
    global order_counter

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "delivery_address": order.delivery_address,
        "status": "pending"
    }

    orders.append(new_order)
    order_counter += 1

    return {"message": "Order placed successfully", "order": new_order}

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = next((o for o in orders if o["order_id"] == order_id), None)

    if not order:
        return {"error": "Order not found"}

    return order

@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):
    order = next((o for o in orders if o["order_id"] == order_id), None)

    if not order:
        return {"error": "Order not found"}

    order["status"] = "confirmed"

    return {"message": "Order confirmed", "order": order}