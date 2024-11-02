from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Data model untuk produk
class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int

# Data model untuk keranjang belanja
class CartItem(BaseModel):
    product_id: int
    quantity: int

# Data model untuk pengguna
class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

# Contoh data sementara
products = [
    Product(id=1, name="T-Shirt EXO", description="Kaos eksklusif EXO", price=250000, stock=10),
    Product(id=2, name="Hoodie EXO", description="Hoodie eksklusif EXO", price=500000, stock=5)
]
cart = []
users = []

# ================== Endpoints Produk ==================

@app.get("/api/products", response_model=List[Product])
async def get_products():
    return products

@app.get("/api/products/{id}", response_model=Product)
async def get_product(id: int):
    for product in products:
        if product.id == id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/api/products", response_model=Product)
async def add_product(product: Product):
    products.append(product)
    return product

@app.put("/api/products/{id}", response_model=Product)
async def update_product(id: int, product: Product):
    for i, p in enumerate(products):
        if p.id == id:
            products[i] = product
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/api/products/{id}")
async def delete_product(id: int):
    global products
    products = [product for product in products if product.id != id]
    return {"detail": "Product deleted"}

# ================== Endpoints Keranjang Belanja ==================

@app.post("/api/cart", response_model=List[CartItem])
async def add_to_cart(item: CartItem):
    cart.append(item)
    return cart

@app.get("/api/cart", response_model=List[CartItem])
async def get_cart():
    return cart

@app.put("/api/cart/{product_id}", response_model=CartItem)
async def update_cart_item(product_id: int, quantity: int):
    for item in cart:
        if item.product_id == product_id:
            item.quantity = quantity
            return item
    raise HTTPException(status_code=404, detail="Item not found in cart")

@app.delete("/api/cart/{product_id}")
async def remove_from_cart(product_id: int):
    global cart
    cart = [item for item in cart if item.product_id != product_id]
    return {"detail": "Item removed from cart"}

# ================== Endpoints Pengguna ==================

@app.post("/api/register", response_model=User)
async def register_user(user: User):
    users.append(user)
    return user

@app.post("/api/login")
async def login_user(email: str, password: str):
    for user in users:
        if user.email == email and user.password == password:
            return {"detail": "Login successful"}
    raise HTTPException(status_code=400, detail="Invalid credentials")

# Jalankan aplikasi dengan Uvicorn jika dijalankan secara lokal
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
