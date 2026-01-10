from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import datetime
import os

Base = declarative_base()
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://mdm_admin:mdm_password@host.docker.internal:5432/mdm_local_db"
)
engine = create_engine(DATABASE_URL)
class Device(Base):
    __tablename__ = "devices"

    device_id = Column(String, primary_key=True, index=True)
    hostname = Column(String)
    os_version = Column(String)
    serial_number = Column(String)
    installed_apps = Column(JSON)  # リストをJSON形式で保存
    last_seen = Column(DateTime, default=datetime.datetime.utcnow)

# 接続先は環境変数から取得（OKEのSecretから注入することを想定）
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/mdm_db")
# engine = create_engine(DATABASE_URL)