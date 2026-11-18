import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-only-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'brewhouse.db')
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'

DEFAULT_SETTINGS = {
    'shop_name': 'Brew House', 'whatsapp_number': '', 'contact_phone': '',
    'address': '', 'working_hours': 'Placeholder: Daily 8:00 AM - 11:00 PM',
    'currency': 'EGP', 'instagram_url': '', 'facebook_url': '', 'maps_embed_url': '',
}
