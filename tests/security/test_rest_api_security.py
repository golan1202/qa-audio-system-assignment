def test_api_rejects_unauthorized_access(api_client):
    resp = api_client.get("/features/realtime", headers={"Authorization": "invalid"})
    assert resp.status_code in (401, 403)
