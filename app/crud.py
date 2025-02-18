from sqlalchemy.orm import Session
from app import models, schemas

# 商品を登録
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# すべての商品を取得
def get_all_products(db: Session):
    return db.query(models.Product).all()

# 商品をコードで検索
def get_product(db: Session, code: str):
    return db.query(models.Product).filter(models.Product.code == str(code)).first()

# 取引を登録
def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    new_transaction = models.Transaction(
        EMP_CD=transaction.EMP_CD,
        STORE_CD=transaction.STORE_CD,
        POS_NO=transaction.POS_NO,
        TOTAL_AMT=transaction.TOTAL_AMT
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    # 取引明細を登録
    for idx, detail in enumerate(transaction.details, start=1):
        new_detail = models.TransactionDetail(
            TRD_ID=new_transaction.TRD_ID,
            DTL_ID=idx,  # 連番を明示
            PRD_ID=detail.PRD_ID,
            PRD_CODE=detail.PRD_CODE,
            PRD_NAME=detail.PRD_NAME,
            PRD_PRICE=detail.PRD_PRICE
        )
        db.add(new_detail)
    
    db.commit()
    return new_transaction
