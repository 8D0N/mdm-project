from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# エージェントから届くデータ
class InventoryReport(BaseModel):
    device_id: str
    hostname: str
    os_version: str
    serial_number: str
    installed_apps: Optional[List[str]] = []

# サーバーからエージェントへ返す命令（宣言型）
class DeviceDirective(BaseModel):
    status: str
    desired_config: Dict[str, Any]
    commands: List[str]