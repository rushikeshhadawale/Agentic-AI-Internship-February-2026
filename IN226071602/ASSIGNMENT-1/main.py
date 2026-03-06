from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Smartphone", "price": 20000, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Headphones", "price": 3000, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Mouse", "price": 800, "category": "Accessories", "in_stock": True},
    {"id": 4, "name": "Keyboard", "price": 1500, "category": "Accessories", "in_stock": True},

    {"id": 5, "name": "Laptop Stand", "price": 1200, "category": "Accessories", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 4500, "category": "Accessories", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 2500, "category": "Electronics", "in_stock": True}
]

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }
@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    filtered_products = [p for p in products if p["category"].lower() == category_name.lower()]

    if not filtered_products:
        return {"error": "No products found in this category"}

    return {
        "category": category_name,
        "products": filtered_products
    }
@app.get("/products/instock")
def get_instock_products():
    instock_products = [p for p in products if p["in_stock"]]

    return {
        "in_stock_products": instock_products,
        "count": len(instock_products)
    }
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
        p for p in products 
        if keyword.lower() in p["name"].lower()
    ]

    if not matched_products:
        return {"message": "No products matched your search"}

    return {
        "matched_products": matched_products,
        "count": len(matched_products)
    }
@app.get("/products/deals")
def get_product_deals():

    cheapest_product = min(products, key=lambda x: x["price"])
    expensive_product = max(products, key=lambda x: x["price"])

    return {
        "best_deal": cheapest_product,
        "premium_pick": expensive_product
    }