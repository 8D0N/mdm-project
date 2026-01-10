from ..schemas.inventory import InventoryReport, DeviceDirective

def calculate_directive(report: InventoryReport) -> DeviceDirective:
    """
    現在の状態(report)を解析し、あるべき姿(directive)を生成する
    """
    # 将来的にはここでDBのポリシーとreportを比較する
    # 例: OSバージョンが古い場合にupdateコマンドを送るなど
    
    return DeviceDirective(
        status="compliant",
        desired_config={
            "inventory_interval": 3600,
            "security_policy": {
                "usb_restricted": True,
                "min_password_len": 8
            }
        },
        commands=[] # 必要に応じて "lock", "reboot" 等を追加
    )