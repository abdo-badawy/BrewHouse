# Brew House (Flask)
## Local setup
```
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # set a long random SECRET_KEY
flask --app app seed      # 30+ PLACEHOLDER demo products
flask --app app create-admin
flask --app app run --debug
```
Admin: `/admin/login`. Set WhatsApp number (digits with country code), phone, address, hours, social URLs, maps embed in **Admin > Settings**. Until the WhatsApp number is set, order buttons show a "not configured" notice.
## Tests
`pytest -q`
## Production (Render / Railway / PythonAnywhere)
Set env vars `SECRET_KEY` (random) and `FLASK_ENV=production`. Start command: `gunicorn "app:create_app()"`. Use a persistent disk for `instance/` and `static/uploads/` (SQLite and uploaded images live there), or point `DATABASE_URI` at a hosted database. Serve over HTTPS. Domain/hosting costs are separate.
