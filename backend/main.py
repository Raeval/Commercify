from fastapi import FastAPI, HTTPException, Depends

from pydantic import BaseModel, EmailStr
from database import Base, engine, get_db
from sqlalchemy.orm import Session
import models

from passlib.context import CryptContext

from services import service, auth_service

from enums import *

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ProductBody(BaseModel):
    name: str
    price: str

class RegisterBody(BaseModel):
    username: str
    email: EmailStr
    password: str
    gender: GenderType

class SignInBody(BaseModel):
    username: str
    password: str

class CreateShopBody(BaseModel):
    shop_name: str
    plan: ShopPlan | None = None

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

@app.post('/auth/register', status_code = 201)
def register(req_body: RegisterBody, db: Session = Depends(get_db)):
    new_user, access_token = auth_service.register(
        req_body.email, req_body.username, req_body.gender, req_body.password, db
    )
    return {
        "message": "User registered successfully",
        "user_id": new_user.user_id,
        "access_token": access_token,
        "token_type": "bearer",
    }

@app.post('/auth/sign-in')
def sign_in(req_body: SignInBody, db: Session = Depends(get_db)):
    user, access_token = auth_service.sign_in(
        req_body.username, req_body.password, db
    )

    return {
        "message": "User Signed In Successfully",
        "user_id": user.user_id,
        "access_token": access_token,
        "token_type": "bearer",
    }

@app.get('/auth/me')
def get_me(
        user: models.User = Depends(auth_service.get_current_user)
    ):
    return {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "gender": user.gender,
    }

@app.get('/orders/{order_id}')
def get_order(
        order_id: int,
        db: Session = Depends(get_db),
        user: models.User = Depends(auth_service.get_current_user),
    ):
    order: models.Order = (
        db.query(models.Order)
            .filter(models.Order.order_id == order_id,
                    models.Order.user_id == user.user_id)
            .first()
    )

    if order:
        return {
            "message": "Order Found",
            "order_id": order.order_id,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "cost_at_purchase": item.cost_at_purchase
                }
                for item in order.items
            ]
        }

    raise HTTPException(status_code=404, detail="Order not found")

@app.post('/shops/create', status_code = 201)
def create_shop(
    req_body: CreateShopBody,
    user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):

    plan = req_body.plan
    if not plan:
        plan = ShopPlan.FREE
    
    new_shop: models.Shop = service.create_shop(
        user,
        req_body.shop_name,
        plan,
        db
    )

    return {
        "message": "Shop created successfully",
        "shop_id": new_shop.shop_id
    }

@app.get('/shops/id/{shop_id}')
def get_shop_by_id(
    shop_id: int,
    _: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    shop: models.Shop = service.get_shop_by_id(shop_id, db)

    return {
        "shop_name": shop.shop_name,
        "shop_id": shop.shop_id,
        "owners": shop.owners,
        "products": [
            {
                "product_id": product.product_id,
                "name": product.product_name,
                "price": product.price,
            }
            for product in shop.products
        ]
    }

@app.get('/shops/name/{shop_name}')
def get_shop_by_name(
    shop_name: str,
    _: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    shop: models.Shop = None 

    return {
        "shop_name": shop.shop_name,
        "shop_id": shop.shop_id,
        "owners": shop.owners,
        "products": [
            {
                "product_id": product.product_id,
                "name": product.product_name,
                "price": product.price,
            }
            for product in shop.products
        ]
    }