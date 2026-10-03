from fastapi.testclient import TestClient
from gateway.main import app

def test_allowlist_and_budget():
    client = TestClient(app)
    good = client.post("/complete", json={"model": "local-small", "prompt": "Summarize the budget.", "max_tokens": 20, "spent": 0}).json()
    assert good["allowed"] is True
    assert good["called_provider"] is False
    assert good["cost"] == 20
    blocked = client.post("/complete", json={"model": "hosted-xl", "prompt": "hi", "max_tokens": 10, "spent": 0}).json()
    assert blocked["allowed"] is False
    over = client.post("/complete", json={"model": "local-large", "prompt": "hi", "max_tokens": 30, "spent": 0}).json()
    assert over["allowed"] is False
