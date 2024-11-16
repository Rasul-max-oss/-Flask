from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import secrets

# Конфигурация приложения и базы данных
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Генерация секретного ключа
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)

# Определение модели товара
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        new_product = Product(name=name,description=description,price=price)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index'))  # Перенаправляем на главную страницу после добавления товара

    return render_template('admin.html',)


if __name__ == '__main__':
    app.run(debug=True)