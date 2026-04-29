import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_get_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_upload(client, tmp_path):
    tmp_path = tmp_path / 'logs'
    tmp_path.mkdir()

    log_file = tmp_path / 'log.txt'

    content = """[2026-04-17 01:54:57 [INFO] [auth-service] Running smoothly
[2026-04-17 01:54:57] [INFO] [dns-service] Connected
[2026-04-17 01:54:57] [INFO] [db-service] Running smoothly
[2026-04-17 01:54:57] [INFO] [db-service] Running smoothly
[2026-04-17 01:54:57] [WARNING] [io-service] no responses
[2026-04-17 01:54:57 [INFO] [dns-service] Connected
[2026-04-17 01:54:57] [ERROR] [dns-service] division by zero
[2026-04-17 01:54:57] [WARNING] [db-service Resources low
[2026-04-17 01:54:57] [ERROR] [io-service] division by zero"""

    log_file.write_text(content, encoding="utf-8")

    with open(str(log_file), "rb") as f:
        response = client.post("/upload", files={"file": f})

    assert response.status_code == 200
    assert "file_path" in response.json()
