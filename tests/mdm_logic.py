from src.app.services.mdm_logic import calculate_directive
from src.app.schemas.inventory import InventoryReport

def test_calculate_directive_logic():
    mock_report = InventoryReport(
        device_id="test-id",
        hostname="test-host",
        os_version="1.0",
        serial_number="SN-TEST"
    )
    directive = calculate_directive(mock_report)
    
    assert directive.status == "compliant"
    assert "inventory_interval" in directive.desired_config