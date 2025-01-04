from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
import locale
import secrets
from products_data import products_data  # Импортируем характеристики товаров

# Установим локаль для правильного форматирования чисел
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

# Конфигурация приложения и базы данных
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Генерация секретного ключа
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///istore.db'
db = SQLAlchemy(app)

# Определение модели товара
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Добавляем связь с ProductSpecification через specifications
    specifications = db.relationship('ProductSpecification', backref='product', lazy=True)


class ProductSpecification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(200), nullable=False)

# Данные для товаров и характеристик (пример)
product_data = [
    # iPhone
    Product(chapter='iphone', name='iPhone 12', description='iPhone 12 с потрясающим экраном и камерой', price=79999),
    Product(chapter='iphone', name='iPhone 13 Pro', description='iPhone 13 Pro с улучшенной камерой и экраном ProMotion', price=99999),
    Product(chapter='iphone', name='iPhone 14', description='iPhone 14 с отличной камерой и мощным процессором', price=89999),
    Product(chapter='iphone', name='iPhone 15 Pro', description='iPhone 15 Pro с новым чипом и возможностями AR', price=119999),

    # Mac
    Product(chapter='Mac', name='MacBook Air', description='Легкий и мощный ноутбук от Apple', price=89999),
    Product(chapter='Mac', name='MacBook Pro', description='Ноутбук с высокой производительностью для профессионалов', price=149999),

    # Watch
    Product(chapter='Watch', name='Apple Watch Ultra', description='Apple Watch Ultra для активного образа жизни', price=99999),
    Product(chapter='Watch', name='Apple Watch Series 8', description='Смарт-часы с отслеживанием здоровья и экстренными функциями', price=49999),
    Product(chapter='Watch', name='Apple Watch SE', description='Доступные умные часы с хорошей производительностью', price=25999),

    # iPad
    Product(chapter='iPad', name='iPad Pro', description='Мощный планшет для профессионалов с поддержкой Apple Pencil', price=79999),
    Product(chapter='iPad', name='iPad Air', description='iPad с хорошим экраном и мощным процессором', price=54999),
    Product(chapter='iPad', name='iPad Mini', description='Компактный и мощный iPad', price=39999),
    Product(chapter='iPad', name='iPad SE', description='Доступный планшет с хорошей производительностью', price=29999),

    # AirPods
    Product(chapter='AirPods', name='AirPods 2nd Gen', description='Беспроводные наушники с хорошим качеством звука', price=9999),
    Product(chapter='AirPods', name='AirPods Pro', description='Активное шумоподавление и идеальная посадка', price=24999),
    Product(chapter='AirPods', name='AirPods Max', description='Беспроводные наушники с высоким качеством звука', price=54999),
]

product_specifications = {
    'iphone': {
        'iPhone 12': [
            {'name': 'Процессор', 'value': 'A14 Bionic'},
            {'name': 'Камера', 'value': '12 МП, ультраширокая и широкоугольная'},
            {'name': 'Экран', 'value': '6.1-дюймовый Super Retina XDR Display'},
            {'name': 'Оперативная память', 'value': '4 ГБ'},
            {'name': 'Память', 'value': '256 ГБ'},
            {'name': 'Аккумулятор', 'value': '2815 мАч'},
            {'name': 'Цвет', 'value': 'Черный'}
        ],
        'iPhone 13 Pro': [
            {'name': 'Процессор', 'value': 'A15 Bionic'},
            {'name': 'Камера', 'value': '12 МП, ультраширокая, широкоугольная и телеобъектив'},
            {'name': 'Экран', 'value': '6.1-дюймовый ProMotion Display'},
            {'name': 'Оперативная память', 'value': '6 ГБ'},
            {'name': 'Память', 'value': '1 ТБ'},
            {'name': 'Аккумулятор', 'value': '3095 мАч'},
            {'name': 'Цвет', 'value': 'Синий'}
        ],
        'iPhone 14': [
            {'name': 'Процессор', 'value': 'A15 Bionic'},
            {'name': 'Камера', 'value': '12 МП, улучшенная широкоугольная'},
            {'name': 'Экран', 'value': '6.1-дюймовый OLED'},
            {'name': 'Оперативная память', 'value': '6 ГБ'},
            {'name': 'Память', 'value': '128 ГБ'},
            {'name': 'Аккумулятор', 'value': '3279 мАч'},
            {'name': 'Цвет', 'value': 'Фиолетовый'}
        ],
        'iPhone 15 Pro': [
            {'name': 'Процессор', 'value': 'A16 Bionic'},
            {'name': 'Камера', 'value': '48 МП, улучшенная телеобъектив'},
            {'name': 'Экран', 'value': '6.1-дюймовый OLED'},
            {'name': 'Оперативная память', 'value': '6 ГБ'},
            {'name': 'Память', 'value': '1 ТБ'},
            {'name': 'Аккумулятор', 'value': '3200 мАч'},
            {'name': 'Цвет', 'value': 'Титан'}
        ]
    },
    'Mac': {
        'MacBook Air': [
            {'name': 'Процессор', 'value': 'M1'},
            {'name': 'Экран', 'value': '13.3 дюйма Retina'},
            {'name': 'Память', 'value': '8 ГБ'},
        ],
        'MacBook Pro': [
            {'name': 'Процессор', 'value': 'M1 Pro'},
            {'name': 'Экран', 'value': '16 дюймов'},
            {'name': 'Память', 'value': '16 ГБ'},
        ],
    },
    # Аналогично для других категорий
}

# Создаем базу данных и таблицы, если их нет
with app.app_context():
    db.create_all()

    # Проверка, если таблица продуктов пустая, то заполняем её
    if not Product.query.first():
        db.session.add_all(product_data)
        db.session.commit()

        # Добавляем характеристики для каждого товара
        for chapter, products in product_specifications.items():
            for product_name, specs in products.items():
                product = Product.query.filter_by(chapter=chapter, name=product_name).first()
                if product:
                    for spec in specs:
                        specification = ProductSpecification(product_id=product.id, name=spec['name'], value=spec['value'])
                        db.session.add(specification)
        db.session.commit()

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

@app.route('/mac')
def mac():
    products = Product.query.filter_by(chapter='Mac').all()
    return render_template('dekstop.html', products=products)

@app.route('/watch')
def watch():
    products = Product.query.filter_by(chapter='Watch').all()
    return render_template('watch.html', products=products)

@app.route('/airpods')
def airpods():
    products = Product.query.filter_by(chapter='AirPods').all()
    return render_template('airpods.html', products=products)


@app.route('/phone')
def phone():
    model_filter = request.args.get('model', '')
    price_filter = request.args.get('price', 0, type=int)
    color_filter = request.args.get('color', '')  # Фильтр по цвету
    memory_filter = request.args.get('memory', '')  # Фильтр по памяти

    products_query = Product.query.filter(Product.chapter == 'iphone')

    # Фильтрация по модели
    if model_filter:
        products_query = products_query.filter(Product.name.like(f'%{model_filter}%'))

    # Фильтрация по цене
    if price_filter > 0:
        products_query = products_query.filter(Product.price <= price_filter)

    # Фильтрация по цвету
    if color_filter:
        products_query = products_query.join(Product.specifications).filter(
            ProductSpecification.name == 'Цвет',
            ProductSpecification.value.like(f'%{color_filter}%')
        )

    # Фильтрация по памяти
    if memory_filter:
        # Проверяем, является ли память в ТБ
        if memory_filter in ['1024', '1ТБ']:
            # Фильтрация для 1 ТБ (1024 ГБ)
            products_query = products_query.join(Product.specifications).filter(
                ProductSpecification.name == 'Память',
                ProductSpecification.value == '1 ТБ'  # Строгое совпадение для ТБ
            )
        else:
            # Фильтрация для ГБ
            products_query = products_query.join(Product.specifications).filter(
                ProductSpecification.name == 'Память',
                ProductSpecification.value.like(f'{memory_filter} ГБ')  # Точное совпадение для ГБ
            )

    # Получаем все товары после применения фильтров
    products = products_query.all()

    # Возвращаем отфильтрованные товары на страницу
    return render_template('phone.html', products=products)
@app.route('/phone/<int:id>')
def get_phone(id):
    iphone = Product.query.filter_by(id=id, chapter='iphone').first()

    if iphone:
        # Получаем характеристики из базы данных для текущей модели iPhone
        product_specs = {spec.name: spec.value for spec in iphone.specifications}

        # Форматируем цену перед отправкой в шаблон
        formatted_price = locale.format_string("%d", iphone.price, grouping=True)

        return render_template('iphone_detail.html', iphone=iphone, formatted_price=formatted_price, specs=product_specs)
    else:
        return abort(404)  # Если айфон не найден, возвращаем ошибку 404


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        chapter = request.form['chapter']
        description = request.form['description']
        price = float(request.form['price'])

        # Создаем новый товар
        new_product = Product(chapter=chapter, name=name, description=description, price=price)
        db.session.add(new_product)
        db.session.commit()

        # Добавляем характеристики товара
        for key, value in request.form.items():
            if key not in ['name', 'chapter', 'description', 'price']:  # игнорируем другие поля
                specification = ProductSpecification(
                    product_id=new_product.id,
                    name=key,
                    value=value
                )
                db.session.add(specification)

        db.session.commit()

        return redirect(url_for('index'))  # Перенаправляем на главную страницу после добавления товара

    return render_template('admin.html')  # Форма для добавления товара

@app.route('/about')
def about():
    images = ["features-01.jpg", "features-02.jpg", "features-03.jpg", "features-04.jpg", "features-05.jpg"]
    return  render_template('about.html', images = images)



if __name__ == '__main__':
    app.run(debug=True)
