import models
from sqlalchemy.orm import Session
from fastapi import HTTPException

from enums import *

def get_shop_by_id(
    shop_id,
    db: Session
):
    shop: models.Shop = (
        db.query(models.Shop)
            .filter(models.Shop.shop_id == shop_id)
            .first()
    )

    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    return shop

def get_shop_by_name(
    shop_name,
    db: Session
):
    shop: models.Shop = (
        db.query(models.Shop)
            .filter(models.Shop.shop_name == shop_name)
            .first()
    )
    
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    return shop

def create_shop(
    user: models.User,
    shop_name: str,
    plan: ShopPlan,
    db: Session
):
    existing_shop = (
        db.query(models.Shop)
            .filter(models.Shop.shop_name == shop_name)
            .first()
    )
    
    if existing_shop:
        raise HTTPException(status_code=409, detail="Shop name not available")
    
    plan = plan
    if not plan:
        plan = ShopPlan.FREE
    
    new_shop = models.Shop(
        shop_name=shop_name,
        plan=plan
    )
    
    db.add(new_shop)
    db.flush()
    
    shop_owner = models.ShopOwner(
        shop_id=new_shop.shop_id,
        user_id=user.user_id,
    )
    
    db.add(shop_owner)
    db.commit()

    return new_shop