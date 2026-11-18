"""Placeholder demo data. All names, prices and texts are SAMPLE content."""
from extensions import db
from models import Category, Product, SiteSetting
from config import DEFAULT_SETTINGS

DATA = 'Hot Coffee|Rich brews from freshly roasted beans.|Espresso:45:Concentrated shot with a velvety crema.;Double Espresso:60:Two shots of espresso.;Cappuccino:75:Espresso, steamed milk and microfoam.;Cafe Latte:80:Espresso with silky steamed milk.;Flat White:80:Ristretto with velvety milk.;Caramel Macchiato:90:Vanilla milk, espresso, caramel.;Cafe Mocha:95:Espresso, chocolate and steamed milk.;Americano:55:Espresso lengthened with hot water.;Turkish Coffee:50:Finely ground coffee brewed in a cezve.;Spanish Latte:95:Espresso, milk and condensed milk.\nCold Coffee|Chilled coffee drinks.|Iced Americano:65:Espresso over ice and water.;Iced Latte:85:Espresso and cold milk over ice.;Iced Caramel Macchiato:95:Vanilla, milk, espresso, caramel.;Cold Brew:90:Steeped 24 hours, smooth and sweet.;Iced Mocha:100:Espresso, chocolate, cold milk.;Frappe Classic:95:Blended iced coffee with cream.;Affogato:110:Vanilla gelato with hot espresso.\nTea|Loose-leaf teas and infusions.|English Breakfast:45:Full-bodied black tea.;Earl Grey:50:Black tea with bergamot.;Green Tea Sencha:50:Delicate green tea.;Chamomile:55:Soothing herbal infusion.;Hibiscus Cooler:55:Tart, refreshing infusion.;Moroccan Mint Tea:50:Green tea with fresh mint.\nDesserts|Fresh cakes and pastries.|Classic Cheesecake:95:Creamy cheesecake on a biscuit base.;Chocolate Fudge Cake:100:Layered chocolate cake.;Tiramisu:105:Espresso-soaked ladyfingers and mascarpone.;Almond Croissant:70:Flaky pastry with almond filling.;Chocolate Chip Cookie:45:Warm cookie with chocolate chunks.;Blueberry Muffin:55:Muffin with blueberries.\nSnacks|Savory bites and sandwiches.|Avocado Toast:85:Sourdough with smashed avocado.;Turkey & Cheese Croissant:90:Smoked turkey and Swiss cheese.;Halloumi Pesto Sandwich:95:Grilled halloumi with basil pesto.;Chicken Caesar Wrap:105:Grilled chicken, romaine, parmesan.'

def seed_data():
    if Category.query.first():
        return 'Database already has data - skipped.'
    for k, v in DEFAULT_SETTINGS.items():
        db.session.add(SiteSetting(setting_key=k, setting_value=v))
    n = 0
    for line in DATA.split('\n'):
        cat, desc, items = line.split('|')
        c = Category(name=cat, description=desc); db.session.add(c); db.session.flush()
        for it in items.split(';'):
            name, price, d = it.split(':')
            db.session.add(Product(name=name, price=float(price), description=d, category_id=c.id)); n += 1
    db.session.commit()
    return f'Seeded {n} demo products.'

if __name__ == '__main__':
    from app import create_app
    with create_app().app_context():
        print(seed_data())
