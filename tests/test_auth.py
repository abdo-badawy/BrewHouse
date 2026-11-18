def test_dashboard_protected(client):
    r = client.get('/admin/'); assert r.status_code == 302 and '/admin/login' in r.location
def test_login_logout(client):
    assert client.post('/admin/login', data={'username': 'boss', 'password': 'bad'}).status_code == 200
    r = client.post('/admin/login', data={'username': 'boss', 'password': 'pass12345'}); assert r.status_code == 302
    assert client.get('/admin/').status_code == 200
    client.post('/admin/logout'); assert client.get('/admin/').status_code == 302
