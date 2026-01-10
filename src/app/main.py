from fastapi import FastAPI
from .schemas.inventory import InventoryReport, DeviceDirective
from .services.mdm_logic import calculate_directive

app = FastAPI(title="Declarative MDM Engine")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/checkin", response_model=DeviceDirective)
async def device_checkin(report: InventoryReport):
    # 1. ログ出力（開発用）
    print(f"[*] Check-in: {report.hostname} ({report.device_id})")
    
    # 2. ロジック実行
    directive = calculate_directive(report)
    
    return directive