import os, sys, io, pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app
from config import Config
from extensions import db
from models import Admin
from seed import seed_data

@pytest.fixture
def app(tmp_path):
    class T(Config):
        TESTING = True; WTF_CSRF_ENABLED = False; SECRET_KEY = 't'
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{tmp_path}/t.db'
        UPLOAD_FOLDER = str(tmp_path / 'up')
    a = create_app(T)
    with a.app_context():
        seed_data(); u = Admin(username='boss'); u.set_password('pass12345'); db.session.add(u); db.session.commit()
    return a

@pytest.fixture
def client(app): return app.test_client()

@pytest.fixture
def admin(client):
    client.post('/admin/login', data={'username': 'boss', 'password': 'pass12345'}); return client
