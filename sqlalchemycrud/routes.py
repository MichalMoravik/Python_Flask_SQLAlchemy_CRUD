from flask import request, jsonify
# import app for routes (@app.route)
from sqlalchemycrud import app
from sqlalchemycrud.models import *

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
    # from request
    delivery_address = request.json['delivery_address']
    status = request.json['status']
    fk_customer_id = request.json['fk_customer_id']
    productsIdArray = request.json['productsIdArray']
    
    # find customer in the database
    customer = Customer.query.filter_by(id=fk_customer_id).first()

    # find products in the database
    products = []
    for product_id in productsIdArray:
        product = Product.query.filter_by(id=product_id).first()
        products.append(product)

    new_order = Order(delivery_address, status, fk_customer_id, customer, products)

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
    # from request
    delivery_address = request.json['delivery_address']
    status = request.json['status']
    fk_customer_id = request.json['fk_customer_id']
    productsIdArray = request.json['productsIdArray']
    
    # find customer in the database
    customer = Customer.query.filter_by(id=fk_customer_id).first()

    # find products in the database
    products = []
    for product_id in productsIdArray:
        product = Product.query.filter_by(id=product_id).first()
        products.append(product)

    order = Order.query.get(id)
    order.delivery_address = delivery_address
    order.status = status
    order.fk_customer_id = fk_customer_id
    order.customer = customer
    order.products = products

    db.session.commit()

    return order_schema.jsonify(order)

# Delete order
@app.route('/order/<id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()

    return order_schema.jsonify(order)
