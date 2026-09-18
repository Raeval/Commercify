from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI()

class ProductBody(BaseModel):
    name: str
    price: str

products = [
{
    "id": "1",
    "name": "apple",
    "price": "5.00",
},
{
    "id": "2",
    "name": "pear",
    "price": "4.50",
},
{
    "id": "3",
    "name": "dragon fruit",
    "price": "5.50",
}]

carts = [{
    "product_id": "1",
    "name": "apple",
    "price": "5.00",
    "quantity": 3,
}]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/products/{item_id}", status_code=200)
async def get_product(item_id: str):
    return find_product(item_id)

@app.post("/products", status_code=201)
async def create_product(product: ProductBody):
    products.append({
        "id": "5",
        "name": product.name,
        "price": product.price
    })
    return product

@app.get("/carts", status_code=200)
async def list_carts():
    return carts

class AddCartBody(BaseModel):
    item_id: str

@app.post("/carts", status_code=201)
async def add_cart(req_body: AddCartBody):
    product = find_product(req_body.item_id)
    new_product = {
        "product_id": product["id"],
        "name": product["name"],
        "price": product["price"],
        "quantity": 1
    }
    carts.append(new_product)
    return new_product

def find_product(item_id: str):
    for product in products:
        if product["id"] == item_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )