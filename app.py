import os, uuid
from flask import Flask, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from PIL import Image
from config import Config, DEFAULT_SETTINGS
from extensions import db, login_manager, csrf
from models import Admin, Product, Category, SiteSetting
from forms import LoginForm, ProductForm

FORMATS = {'PNG': 'png', 'JPEG': 'jpg', 'WEBP': 'webp'}

def save_image(fs):
    """Validate extension AND real image content; return safe unique filename or None."""
    if not fs or not fs.filename:
        return None
    if fs.filename.rsplit('.', 1)[-1].lower() not in current_app.config['ALLOWED_EXTENSIONS']:
        raise ValueError('Only PNG, JPG or WEBP images are allowed.')
    try:
        img = Image.open(fs.stream); fmt = img.format; img.verify(); fs.stream.seek(0)
    except Exception:
        raise ValueError('File is not a valid image.')
    if fmt not in FORMATS:
        raise ValueError('Unsupported image type.')
    name = f'{uuid.uuid4().hex}.{FORMATS[fmt]}'
    fs.save(os.path.join(current_app.config['UPLOAD_FOLDER'], name))
    return name

def remove_image(name):
    if name:
        p = os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.basename(name))
        if os.path.isfile(p): os.remove(p)

def get_settings():
    s = dict(DEFAULT_SETTINGS)
    s.update({r.setting_key: r.setting_value or '' for r in SiteSetting.query.all()})
    return s

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)
    db.init_app(app); login_manager.init_app(app); csrf.init_app(app)
    with app.app_context():
        db.create_all()

    @app.cli.command('create-admin')
    def create_admin():
        """Create an admin account (prompts for password)."""
        import click
        u = click.prompt('Username')
        p = click.prompt('Password (min 8 chars)', hide_input=True, confirmation_prompt=True)
        if len(p) < 8: raise click.ClickException('Password too short.')
        if Admin.query.filter_by(username=u).first(): raise click.ClickException('User exists.')
        a = Admin(username=u); a.set_password(p); db.session.add(a); db.session.commit()
        click.echo('Admin created.')

    @app.cli.command('seed')
    def seed():
        """Load placeholder demo data (only if the DB is empty)."""
        from seed import seed_data
        print(seed_data())

    @app.context_processor
    def inject():
        return dict(site=get_settings())

    @app.errorhandler(404)
    def nf(e): return render_template('error.html', code=404, msg='Page not found'), 404
    @app.errorhandler(413)
    def big(e): return render_template('error.html', code=413, msg='File too large (max 5 MB)'), 413

    # ---- public ----
    @app.route('/')
    def index():
        feat = Product.query.filter_by(is_available=True).order_by(Product.id).limit(6).all()
        return render_template('index.html', featured=feat)

    @app.route('/menu')
    def menu():
        cats = Category.query.order_by(Category.id).all()
        data = [(c, [p for p in c.products if p.is_available]) for c in cats]
        return render_template('menu.html', data=[d for d in data if d[1]])

    @app.route('/about')
    def about(): return render_template('about.html')
    @app.route('/contact')
    def contact(): return render_template('contact.html')

    # ---- admin ----
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if current_user.is_authenticated: return redirect(url_for('admin_dashboard'))
        form = LoginForm()
        if form.validate_on_submit():
            a = Admin.query.filter_by(username=form.username.data.strip()).first()
            if a and a.check_password(form.password.data):
                login_user(a)
                nxt = request.args.get('next', '')
                return redirect(nxt if nxt.startswith('/admin') else url_for('admin_dashboard'))
            flash('Invalid username or password.', 'danger')
        return render_template('admin/login.html', form=form)

    @app.route('/admin/logout', methods=['POST'])
    @login_required
    def admin_logout():
        logout_user(); flash('Logged out.', 'info')
        return redirect(url_for('admin_login'))

    @app.route('/admin/')
    @login_required
    def admin_dashboard():
        q = Product.query
        return render_template('admin/dashboard.html', total=q.count(),
            avail=q.filter_by(is_available=True).count(),
            unavail=q.filter_by(is_available=False).count(), cats=Category.query.count())

    @app.route('/admin/products')
    @login_required
    def admin_products():
        return render_template('admin/products.html',
            products=Product.query.order_by(Product.category_id, Product.name).all())

    def handle_form(product=None):
        form = ProductForm(obj=product)
        form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name)]
        if form.validate_on_submit():
            try:
                img = save_image(request.files.get('image_file'))
            except ValueError as e:
                flash(str(e), 'danger'); return form, None
            p = product or Product()
            p.name = form.name.data.strip()
            p.description = (form.description.data or '').strip()
            p.price = float(form.price.data); p.category_id = form.category_id.data
            p.is_available = form.is_available.data
            if img:
                remove_image(p.image_filename); p.image_filename = img
            db.session.add(p); db.session.commit()
            return form, p
        return form, None

    @app.route('/admin/products/add', methods=['GET', 'POST'])
    @login_required
    def admin_add_product():
        form, p = handle_form()
        if p: flash('Product added.', 'success'); return redirect(url_for('admin_products'))
        return render_template('admin/add_product.html', form=form)

    @app.route('/admin/products/<int:pid>/edit', methods=['GET', 'POST'])
    @login_required
    def admin_edit_product(pid):
        product = db.get_or_404(Product, pid)
        form, p = handle_form(product)
        if p: flash('Product updated.', 'success'); return redirect(url_for('admin_products'))
        return render_template('admin/edit_product.html', form=form, product=product)

    @app.route('/admin/products/<int:pid>/delete', methods=['POST'])
    @login_required
    def admin_delete_product(pid):
        p = db.get_or_404(Product, pid)
        remove_image(p.image_filename); db.session.delete(p); db.session.commit()
        flash('Product deleted.', 'success')
        return redirect(url_for('admin_products'))

    @app.route('/admin/settings', methods=['GET', 'POST'])
    @login_required
    def admin_settings():
        if request.method == 'POST':
            for k in DEFAULT_SETTINGS:
                v = request.form.get(k, '').strip()[:500]
                if k.endswith('_url') and v and not v.startswith(('https://', 'http://')):
                    flash(f'{k} must start with https://', 'danger'); break
                row = SiteSetting.query.filter_by(setting_key=k).first() or SiteSetting(setting_key=k)
                row.setting_value = v; db.session.add(row)
            else:
                db.session.commit(); flash('Settings saved.', 'success')
                return redirect(url_for('admin_settings'))
        return render_template('admin/settings.html', keys=list(DEFAULT_SETTINGS))
    return app

if __name__ == '__main__':
    create_app().run(debug=os.environ.get('FLASK_ENV') != 'production')
