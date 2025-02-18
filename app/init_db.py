from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Product

# 商品データを登録
def init_db():
    db = SessionLocal()
    
    # 初期データ（POSで利用する商品コード一覧）
    product_list = [
        {"code": "123456", "name": "りんご", "price": 150},
        {"code": "654321", "name": "バナナ", "price": 100},
        {"code": "111222", "name": "オレンジ", "price": 120},
    ]

    for p in product_list:
        db_product = Product(code=p["code"], name=p["name"], price=p["price"])
        db.add(db_product)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
