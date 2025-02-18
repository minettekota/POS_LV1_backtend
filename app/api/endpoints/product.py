from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/api", tags=["products"])

# すべての商品を取得
@router.get("/products", response_model=list[schemas.Product])
async def read_products(db: Session = Depends(database.get_db)):
    products = crud.get_all_products(db)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products

# 特定の商品コードで検索
@router.get("/products/{code}", response_model=schemas.Product)
async def read_product(code: str, db: Session = Depends(database.get_db)):
    product = crud.get_product(db, code)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
