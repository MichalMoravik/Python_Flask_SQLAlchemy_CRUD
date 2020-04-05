# this will go to __init__.py file and import db
from sqlalchemycrud import db, ma

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


############# Orders - Products junction table #############
orders_products = db.Table('orders_products',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)


############# Order Class/Model #############
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery_address = db.Column(db.String(400))
    status = db.Column(db.Integer)
    # FK column pointing to customer table in DB (that's why lowercase)
    fk_customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    # pseudo column for Order - Product junction
    products = db.relationship('Product', secondary = orders_products, backref = db.backref('orders', lazy = 'dynamic'))

    def __init__(self, delivery_address, status, fk_customer_id):
        self.delivery_address = delivery_address
        self.status = status
        self.fk_customer_id = fk_customer_id

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'delivery_address', 'status', 'fk_customer_id')

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)