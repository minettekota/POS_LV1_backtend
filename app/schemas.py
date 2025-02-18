from pydantic import BaseModel
from typing import List
from datetime import datetime

class Product(BaseModel):
    code: str
    name: str
    price: float
    description: str | None = None


# ✅ 商品マスタスキーマ
class ProductBase(BaseModel):
    CODE: str
    NAME: str
    PRICE: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    PRD_ID: int

    class Config:
        from_attributes = True  # ✅ ORM モード

# ✅ 取引明細スキーマ
class TransactionDetailBase(BaseModel):
    PRD_ID: int
    PRD_CODE: str
    PRD_NAME: str
    PRD_PRICE: int

class TransactionDetailCreate(TransactionDetailBase):
    pass

class TransactionDetailResponse(TransactionDetailBase):
    DTL_ID: int

    class Config:
        from_attributes = True  # ✅ ORM モード

# ✅ 取引スキーマ
class TransactionBase(BaseModel):
    EMP_CD: str
    STORE_CD: str
    POS_NO: str
    TOTAL_AMT: int

class TransactionCreate(TransactionBase):
    details: List[TransactionDetailCreate]  # ✅ 修正

class TransactionResponse(TransactionBase):
    TRD_ID: int
    DATETIME: datetime
    details: List[TransactionDetailResponse]  # ✅ 修正（Response なので `TransactionDetailResponse` を使う）

    class Config:
        from_attributes = True  # ✅ ORM モード

# ✅ **購入リクエストスキーマ (エラーの原因だった `PurchaseRequest` を追加)**
class PurchaseRequest(BaseModel):
    items: List[TransactionDetailCreate]  # ✅ 商品リスト
