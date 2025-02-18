import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app.database import SessionLocal, engine
from app import models
import logging
from app.api.endpoints.product import router as product_router

# モデルの作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(product_router, prefix="/api")

# ロギング設定
logging.basicConfig(level=logging.INFO)

# CORS設定 (Next.jsのフロントエンドと通信するため)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB セッションを取得する関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 商品取得API
@app.get("/api/products/{code}")
def get_product(code: str, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.code == code).first()
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "CODE": product.code,
        "NAME": product.name,
        "PRICE": product.price,
        "PRD_ID": product.prd_id
    }

# 取引登録API
@app.post("/api/transactions")
def create_transaction(transaction: dict, db: Session = Depends(get_db)):
    try:
        new_transaction = models.Transaction(
            emp_cd=transaction["emp_cd"],
            store_cd=transaction["store_cd"],
            pos_no=transaction["pos_no"],
            total_amt=transaction["total_amt"]
        )
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        return {"message": "Transaction created successfully", "transaction_id": new_transaction.trd_id}
    
    except Exception as e:
        logging.error(f"Transaction creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Transaction creation failed")

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# FastAPIの起動
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
