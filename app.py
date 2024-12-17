from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import secrets

# Конфигурация приложения и базы данных
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Генерация секретного ключа
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///AppleShop.db'
db = SQLAlchemy(app)





# Определение модели товара
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter = db.Column(db.String(100), nullable=False)#раздел т.е что это телефон компьтер или наушник
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)


# Создаем несколько товаров для каждой категории
products = [
    # Mac
    Product(chapter='Mac', name='MacBook Air', description='Легкий и мощный ноутбук от Apple', price=89999),
    Product(chapter='Mac', name='MacBook Pro', description='Ноутбук с высокой производительностью для профессионалов',
            price=149999),

    # iPhone
    Product(chapter='iphone', name='iPhone 12', description='iPhone 12 с потрясающим экраном и камерой', price=79999),
    Product(chapter='iphone', name='iPhone 13 Pro',
            description='iPhone 13 Pro с улучшенной камерой и экраном ProMotion', price=99999),
    Product(chapter='iphone', name='iPhone 14', description='iPhone 14 с отличной камерой и мощным процессором',
            price=89999),
    Product(chapter='iphone', name='iPhone 15 Pro', description='iPhone 15 Pro с новым чипом и возможностями AR',
            price=119999),

    # Watch
    Product(chapter='Watch', name='Apple Watch Ultra', description='Apple Watch Ultra для активного образа жизни',
            price=99999),
    Product(chapter='Watch', name='Apple Watch Series 8',
            description='Смарт-часы с отслеживанием здоровья и экстренными функциями', price=49999),
    Product(chapter='Watch', name='Apple Watch SE', description='Доступные умные часы с хорошей производительностью',
            price=25999),

    # iPad
    Product(chapter='iPad', name='iPad Pro', description='Мощный планшет для профессионалов с поддержкой Apple Pencil',
            price=79999),
    Product(chapter='iPad', name='iPad Air', description='iPad с хорошим экраном и мощным процессором', price=54999),
    Product(chapter='iPad', name='iPad Mini', description='Компактный и мощный iPad', price=39999),
    Product(chapter='iPad', name='iPad SE', description='Доступный планшет с хорошей производительностью', price=29999),

    # AirPods
    Product(chapter='AirPods', name='AirPods 2nd Gen', description='Беспроводные наушники с хорошим качеством звука',
            price=9999),
    Product(chapter='AirPods', name='AirPods Pro', description='Активное шумоподавление и идеальная посадка',
            price=24999),
    Product(chapter='AirPods', name='AirPods Max', description='Беспроводные наушники с высоким качеством звука',
            price=54999),
]


# Создаем базу данных и таблицы
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    products = Product.query.all()  # Получаем все товары из базы данных
    return render_template('index.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if product:
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append({'id': product.id, 'name': product.name, 'price': product.price})
        session.modified = True
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)


@app.route('/dekstop')
def dekstop():
    model_filter = request.args.get('model', '')
    price_filter = request.args.get('price', 0, type=int)

    products_query = Product.query.filter(Product.chapter == 'Mac')
    if model_filter:
        products_query = products_query.filter(Product.name.like(f'%{model_filter}%'))

        # Фильтруем по цене
    if price_filter > 0:
        products_query = products_query.filter(Product.price <= price_filter)
        # Получаем отфильтрованные товары
    products = products_query.all()
    # products = Product.query.filter(Product.chapter == 'Айфон').all()  # Получаем все товары, у которых chapter равен 'айфон'
    return render_template('dekstop.html', products=products)


@app.route('/phone')
def phone():
    # Получаем фильтры из GET-запроса
    model_filter = request.args.get('model', '')
    price_filter = request.args.get('price', 0, type=int)

    products_query = Product.query.filter(Product.chapter == 'iphone')

    # Фильтруем по модели
    if model_filter:
        products_query = products_query.filter(Product.name.like(f'%{model_filter}%'))

    # Фильтруем по цене
    if price_filter > 0:
        products_query = products_query.filter(Product.price <= price_filter)
        # Получаем отфильтрованные товары
    products = products_query.all()
    #products = Product.query.filter(Product.chapter == 'Айфон').all()  # Получаем все товары, у которых chapter равен 'айфон'
    return render_template('phone.html', products=products)

@app.route('/about')
def about():
    images = ["features-01.jpg", "features-02.jpg", "features-03.jpg", "features-04.jpg", "features-05.jpg"]
    return  render_template('about.html', images = images)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        name = request.form['name']
        chapter = request.form['chapter']
        description = request.form['description']
        price = request.form['price']

        new_product = Product(chapter=chapter,name=name,description=description,price=price)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index'))  # Перенаправляем на главную страницу после добавления товара

    return render_template('admin.html',)


if __name__ == '__main__':
    app.run(debug=True)