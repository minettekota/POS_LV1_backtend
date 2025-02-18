import os
from fastapi import FastAPI, HTTPException
import mysql.connector
from urllib.parse import quote

app = FastAPI()

# SSL証明書のパス
SSL_CERT_PATH = "C:/Users/me08t/Step4/POS_LV1/backend/DigiCertGlobalRootCA.crt.pem"

# Azure MySQL の接続情報
db_config = {
    "host": "tech0-gen-8-step4-db-3.mysql.database.azure.com",
    "user": "Tech0Gen8TA3",
    "password": quote("gen8-1-ta@3"),
    "database": "pos_db_kotakota",
    "ssl_ca": SSL_CERT_PATH
}

# DB接続関数
def get_db_connection():
    return mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        ssl_ca=db_config["ssl_ca"]
    )

@app.get("/api/products/{product_code}")
async def get_product(product_code: str):
    """ 指定された商品コードの商品情報を取得 """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 商品情報を取得
        query = "SELECT * FROM products WHERE code = %s"
        cursor.execute(query, (product_code,))
        product = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

@app.get("/")
async def root():
    return {"message": "Hello FastAPI, MySQL connected!"}
