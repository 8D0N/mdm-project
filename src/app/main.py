from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, sessionmaker
from .models.device import Device, engine, Base
from .schemas.inventory import InventoryReport, DeviceDirective
from .services.mdm_logic import calculate_directive
import datetime
import os

# テーブル作成
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app = FastAPI()

# テンプレート設定 (`templetes` フォルダを使用)
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templetes"))

# DBセッションの依存注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    return templates.TemplateResponse("index.html", {"request": request, "devices": devices})


@app.post("/v1/checkin", response_model=DeviceDirective)
async def device_checkin(report: InventoryReport, db: Session = Depends(get_db)):
    # 1. DBから既存のデバイスを検索
    db_device = db.query(Device).filter(Device.device_id == report.device_id).first()

    if db_device:
        # 更新 (Upsert)
        db_device.hostname = report.hostname
        db_device.os_version = report.os_version
        db_device.installed_apps = report.installed_apps
        db_device.last_seen = datetime.datetime.utcnow()
    else:
        # 新規登録
        db_device = Device(
            device_id=report.device_id,
            hostname=report.hostname,
            os_version=report.os_version,
            serial_number=report.serial_number,
            installed_apps=report.installed_apps
        )
        db.add(db_device)

    # 変更をコミット
    db.commit()

    # 2. 宣言型命令の生成（共通ロジックに委譲）
    directive = calculate_directive(report)
    return directive