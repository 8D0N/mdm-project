import pytest
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_health_check():
    """ヘルスチェックエンドポイントのテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_device_checkin_valid():
    """正常なインベントリ報告に対するテスト"""
    payload = {
        "device_id": "dev-12345",
        "hostname": "WIN-DESKTOP-01",
        "os_version": "Windows 11 Pro 22H2",
        "serial_number": "SN-987654321",
        "installed_apps": ["Chrome", "VSCode"]
    }
    response = client.post("/v1/checkin", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "compliant"
    assert "desired_config" in data
    assert data["desired_config"]["security_policy"]["usb_restricted"] is True

def test_device_checkin_invalid_payload():
    """不正なデータ形式（バリデーションエラー）のテスト"""
    # device_id が欠落している場合
    incomplete_payload = {
        "hostname": "Incomplete-PC"
    }
    response = client.post("/v1/checkin", json=incomplete_payload)
    assert response.status_code == 422  # Unprocessable Entity