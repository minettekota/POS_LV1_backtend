import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv()

# Azure MySQL 接続情報
db_config = {
    "host": os.getenv("MYSQL_HOST", "tech0-gen-8-step4-db-3.mysql.database.azure.com"),
    "user": os.getenv("MYSQL_USER", "Tech0Gen8TA3"),
    "password": quote(os.getenv("MYSQL_PASSWORD", "gen8-1-ta@3")),  # ✅ URL エンコード
    "database": os.getenv("MYSQL_DATABASE", "pos_db_kotakota"),
    "ssl_ca": os.getenv("SSL_CA_CERT", os.path.join(os.path.dirname(__file__), "DigiCertGlobalRootCA.crt.pem"))  # ✅ 証明書のフルパス
}

# ✅ SSL 証明書のパスをフルパスで指定
DEFAULT_SSL_CA_PATH = "C:/Users/me08t/Step4/POS_LV1/backend/DigiCertGlobalRootCA.crt.pem"

# SSL 証明書の存在を確認
if not os.path.exists(db_config["ssl_ca"]):
    raise FileNotFoundError(f"❌ SSL 証明書が見つかりません: {db_config['ssl_ca']}")

# SQLAlchemy の接続 URL
DATABASE_URL = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

# ✅ SQLAlchemy エンジンの作成
engine = create_engine(
    DATABASE_URL,
    connect_args={"ssl_ca": db_config["ssl_ca"]}  # ✅ SSL 証明書を設定
)

# ✅ セッション作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ DB セッション取得関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
