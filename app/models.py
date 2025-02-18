from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

# 商品マスタテーブル
class Product(Base):
    __tablename__ = "m_product_kota"

    prd_id = Column(Integer, primary_key=True, index=True)
    code = Column(String(13), unique=True, index=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint('code', name='uq_product_code'),)

# 取引テーブル
class Transaction(Base):
    __tablename__ = "m_transaction_kota"

    trd_id = Column(Integer, primary_key=True, index=True)
    datetime = Column(TIMESTAMP, default=func.now())
    emp_cd = Column(String(10), nullable=False)
    store_cd = Column(String(5), nullable=False)
    pos_no = Column(String(3), nullable=False)
    total_amt = Column(Integer, nullable=False)

    details = relationship("TransactionDetail", back_populates="transaction")

# 取引明細テーブル
class TransactionDetail(Base):
    __tablename__ = "m_transaction_detail_kota"

    dtl_id = Column(Integer, primary_key=True, index=True)
    trd_id = Column(Integer, ForeignKey("m_transaction_kota.trd_id"), index=True)
    prd_id = Column(Integer, ForeignKey("m_product_kota.prd_id"))
    prd_code = Column(String(13))
    prd_name = Column(String(50))
    prd_price = Column(Integer)

    transaction = relationship("Transaction", back_populates="details")
    product = relationship("Product")
