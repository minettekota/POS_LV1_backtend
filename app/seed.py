from app.database import SessionLocal
from app.models import Product

def seed_products():
    db = SessionLocal()

    # 既にデータが存在するか確認（重複登録を避ける）
    if db.query(Product).first():
        print("データは既に存在します。")
        db.close()
        return

    # サンプルデータ登録
    products = [
        Product(code="1234567890123", name="商品A", price=100),
        Product(code="2345678901234", name="商品B", price=200),
        Product(code="3456789012345", name="商品C", price=300),
    ]
    db.add_all(products)
    db.commit()
    db.close()
    print("サンプルデータを登録しました。")

if __name__ == "__main__":
    seed_products()
