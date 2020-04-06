from flask import request, jsonify
# from __init__.py file import app - for routes (@app.route)
from sqlalchemycrud import app
from sqlalchemycrud.models import *
from os import path
# current script name
script_name = path.basename(__file__)

############# Product #############
# Create a product
@app.route('/product', methods=['POST'])
def add_product():
    try:
        name = request.json['name']
        desc = request.json['desc']
        price = request.json['price']
        qty = request.json['qty']

        new_product = Product(name, desc, price, qty)
        db.session.add(new_product)
        db.session.commit()

        return product_schema.jsonify(new_product)
    except Exception as e:
        print(f"******* Error in {script_name} add_product() *******")
        print(f"Error: {e}")
        return jsonify("Cannot add product!"), 500

# Get all products
@app.route('/product', methods=['GET'])
def get_products():
    try:
        all_products = Product.query.all()
        result = products_schema.dump(all_products)
        return jsonify(result)
    except Exception as e:
        print(f"******* Error in {script_name}: get_products() *******")
        print(f"Error: {e}")
        return jsonify("Cannot get products!"), 500

# Get one product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    try:
        product = Product.query.get(id)
        return product_schema.jsonify(product)
    except Exception as e:
        print(f"******* Error in {script_name}: get_product(id) *******")
        print(f"Error: {e}")
        return jsonify("Cannot get product!"), 500

# Update a product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    try:
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
    except Exception as e:
        print(f"******* Error in {script_name}: update_product(id) *******")
        print(f"Error: {e}")
        return jsonify("Cannot update product!"), 500

# Delete product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()

        return product_schema.jsonify(product)
    except Exception as e:
        print(f"******* Error in {script_name}: delete_product(id) *******")
        print(f"Error: {e}")
        return jsonify("Cannot delete product!"), 500



############# Customer #############
# Create a customer
@app.route('/customer', methods=['POST'])
def add_customer():
    try:
        name = request.json['name']
        email = request.json['email']

        new_customer = Customer(name, email)
        db.session.add(new_customer)
        db.session.commit()

        return customer_schema.jsonify(new_customer)
    except Exception as e:
        print(f"******* Error in {script_name}: add_customer() *******")
        print(f"Error: {e}")
        return jsonify("Cannot add customer!"), 500

# Get all customers
@app.route('/customer', methods=['GET'])
def get_customers():
    try:
        all_customers = Customer.query.all()
        result = customers_schema.dump(all_customers)
        return jsonify(result)
    except Exception as e:
        print(f"******* Error in {script_name}: get_customers() *******")
        print(f"Error: {e}")
        return jsonify("Cannot get customers!"), 500

# Get one customer
@app.route('/customer/<id>', methods=['GET'])
def get_customer(id):
    try:
        customer = Customer.query.get(id)
        return customer_schema.jsonify(customer)
    except Exception as e:
        print(f"******* Error in {script_name}: get_customer(id) *******")
        print(f"Error: {e}")
        return jsonify("Cannot get customer!"), 500

# Update a customer
@app.route('/customer/<id>', methods=['PUT'])
def update_customer(id):
    try:
        name = request.json['name']
        email = request.json['email']

        customer = Customer.query.get(id)
        customer.name = name
        customer.email = email

        db.session.commit()

        return customer_schema.jsonify(customer)
    except Exception as e:
        print(f"******* Error in {script_name}: update_customer(id) *******")
        print(f"Error: {e}")
        return jsonify("Cannot update customer!"), 500

# Delete customer
@app.route('/customer/<id>', methods=['DELETE'])
def delete_customer(id):
    try:
        customer = Customer.query.get(id)
        db.session.delete(customer)
        db.session.commit()

        return customer_schema.jsonify(customer)
    except Exception as e:
        print(f"******* Error in {script_name}: delete_customer(id) *******")
        print(f"Error: {e}")
        return jsonify("Cannot delete customer!"), 500


############# Order #############
# Create a order
@app.route('/order', methods=['POST'])
def add_order():
    try:
        delivery_address = request.json['delivery_address']
        status = request.json['status']
        fk_customer_id = request.json['fk_customer_id']
        productsIdArray = request.json['productsIdArray']
        
        # find customer in the database by id
        customer = Customer.query.filter_by(id=fk_customer_id).first()

        # find products in the database by id
        products = []
        for product_id in productsIdArray:
            product = Product.query.filter_by(id=product_id).first()
            products.append(product)

        new_order = Order(delivery_address, status, fk_customer_id, customer, products)

        db.session.add(new_order)
        db.session.commit()

        return order_schema.jsonify(new_order)
    except Exception as e:
        print(f"******* Error in {script_name}: add_order() *******")
        print(f"Error: {e}")
        return jsonify("Cannot add order!"), 500

# Get all orders
@app.route('/order', methods=['GET'])
def get_orders():
    try:
        all_orders = Order.query.all()
        result = orders_schema.dump(all_orders)
        return jsonify(result)
    except Exception as e:
        print(f"******* Error in {script_name}: get_orders() *******")
        print(f"Error: {e}")
        return jsonify("Cannot get orders!"), 500

# Get one order
@app.route('/order/<id>', methods=['GET'])
def get_order(id):
    try:
        order = Order.query.get(id)
        return order_schema.jsonify(order)
    except Exception as e:
        print(f"******* Error in {script_name}: get_order(id) *******")
        print(f"Error: {e}")
        return jsonify("Cannot get order!"), 500

# Update a order
@app.route('/order/<id>', methods=['PUT'])
def update_order(id):
    try:
        delivery_address = request.json['delivery_address']
        status = request.json['status']
        fk_customer_id = request.json['fk_customer_id']
        productsIdArray = request.json['productsIdArray']
        
        # find customer in the database by id
        customer = Customer.query.filter_by(id=fk_customer_id).first()

        # find products in the database by id
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
    except Exception as e:
        print(f"******* Error in {script_name}: update_order(id) *******")
        print(f"Error: {e}")
        return jsonify("Cannot update product!"), 500

# Delete order
@app.route('/order/<id>', methods=['DELETE'])
def delete_order(id):
    try:
        order = Order.query.get(id)
        db.session.delete(order)
        db.session.commit()

        return order_schema.jsonify(order)
    except Exception as e:
        print(f"******* Error in {script_name}: delete_order(id) *******")
        print(f"Error: {e}")
        return jsonify("Cannot delete order!"), 500
