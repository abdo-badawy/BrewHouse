from models import Product
def test_public_pages(client):
    for u in ['/', '/menu', '/about', '/contact']: assert client.get(u).status_code == 200
    assert b'Your Daily Dose of Happiness' in client.get('/').data
def test_seed_count_and_404(app, client):
    with app.app_context(): assert Product.query.count() >= 30
    assert client.get('/nope').status_code == 404
def test_unavailable_hidden(app, client):
    from extensions import db
    with app.app_context():
        p = Product.query.filter_by(name='Espresso').first(); p.is_available = False; db.session.commit()
    assert b'data-name="Espresso"' not in client.get('/menu').data
def test_whatsapp_unconfigured_flag(client):
    assert b'wa:""' in client.get('/menu').data
