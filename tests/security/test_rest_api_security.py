def test_api_rejects_unauthorized_access(api_client):
    client, api_base = api_client
    resp = client.get(f"{api_base}/features/realtime", headers={"Authorization": "invalid"})
    assert resp.status_code in (401, 403)
