from fastapi.testclient import TestClient
import os

# Make sure DB is disabled for tests
os.environ['DISABLE_DB'] = 'true'

from app.main import app  # noqa: E402

client = TestClient(app)

def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    j = r.json()
    assert 'status' in j
