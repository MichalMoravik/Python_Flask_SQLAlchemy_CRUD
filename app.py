from flask import Flask, request, jsonify
# SQLAlchemy provides SQL syntax in Python
from flask_sqlalchemy import SQLAlchemy
# Marshmallow converts complex datatypes, such as objects, to and from native Python datatypes.
from flask_marshmallow import Marshmallow
import os

# Init server
app = Flask(__name__)

############# DATABASE #############
# Setup sql-alchemy database URI to locate a database file
# Database file will be in a root directory
basedir = os.path.abspath(os.path.dirname(__file__))
# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init database
db = SQLAlchemy(app)
# Init marshmallow
ma = Marshmallow(app)

# for attr in dir(db):
#     print(f"{attr}")

############# MODELS #############
############# Product Class/Model #############
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # index param. is indexing 
    name = db.Column(db.String(100), unique=True, index=True)
    desc = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, desc, price, qty):
        self.name = name
        self.desc = desc
        self.price = price
        self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'desc', 'price', 'qty')

# Init schema
# For one product manipulation
product_schema = ProductSchema()
# For many products manipulation
products_schema = ProductSchema(many=True)


############# Customer Class/Model #############
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(255), unique=True)
    # pseudo column (not visible) creating in Order class and 
    # this will be a "customer" (backref) of the Order class
    orders = db.relationship('Order', backref='customer')

    def __init__(self, name, email):
        self.name = name
        self.email = email

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


############# Order Class/Model #############
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery_address = db.Column(db.String(400))
    status = db.Column(db.Integer)
    # FK column pointing to customer table in DB (that's why lowercase)
    fk_customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    # pseudo column for Order - Product junction
    products = db.relationshop('Product', secondary = orders_products, backref = db.backref('orders', lazy = 'dynamic'))

    def __init__(self, delivery_address, status, fk_customer_id):
        self.delivery_address = delivery_address
        self.status = status
        self.fk_customer_id = fk_customer_id

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'delivery_address', 'status', 'fk_customer_id')

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


############# Orders - Products junction table #############
orders_products = db.Table('orders_products',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)


############# ROUTES #############
############# Product #############
# Create a product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    desc = request.json['desc']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, desc, price, qty)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Get all products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Get one product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Update a product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    name = request.json['name']
    desc = request.json['desc']
    price = request.json['price']
    qty = request.json['qty']

    product = Product.query.get(id)
    product.name = name
    product.desc = desc
    product.price = price
    product.qty = qty

    db.session.commit()

    return product_schema.jsonify(product)

# Delete product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)



############# Customer #############
# Create a customer
@app.route('/customer', methods=['POST'])
def add_customer():
    name = request.json['name']
    email = request.json['email']

    new_customer = Customer(name, email)
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer)

# Get all customers
@app.route('/customer', methods=['GET'])
def get_customers():
    all_customers = Customer.query.all()
    result = customers_schema.dump(all_customers)
    return jsonify(result)

# Get one customer
@app.route('/customer/<id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get(id)
    return customer_schema.jsonify(customer)

# Update a customer
@app.route('/customer/<id>', methods=['PUT'])
def update_customer(id):
    name = request.json['name']
    email = request.json['email']

    customer = Customer.query.get(id)
    customer.name = name
    customer.email = email

    db.session.commit()

    return customer_schema.jsonify(customer)

# Delete customer
@app.route('/customer/<id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    db.session.delete(customer)
    db.session.commit()

    return customer_schema.jsonify(customer)


############# Order #############
# Create a order
@app.route('/order', methods=['POST'])
def add_order():
    delivery_address = request.json['delivery_address']
    status = request.json['status']
    fk_customer_id = request.json['fk_customer_id']

    new_order = Order(delivery_address, status, fk_customer_id)
    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order)

# Get all orders
@app.route('/order', methods=['GET'])
def get_orders():
    all_orders = Order.query.all()
    result = orders_schema.dump(all_orders)
    return jsonify(result)

# Get one order
@app.route('/order/<id>', methods=['GET'])
def get_order(id):
    order = Order.query.get(id)
    return order_schema.jsonify(order)

# Update a order
@app.route('/order/<id>', methods=['PUT'])
def update_order(id):
    delivery_address = request.json['delivery_address']
    status = request.json['status']
    fk_customer_id = request.json['fk_customer_id']

    order = Order.query.get(id)
    order.delivery_address = delivery_address
    order.status = status
    order.fk_customer_id = fk_customer_id

    db.session.commit()

    return order_schema.jsonify(order)

# Delete order
@app.route('/order/<id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()

    return order_schema.jsonify(order)


############# MAIN #############
# Run server
if __name__ == '__main__':
    app.run(debug=True)
