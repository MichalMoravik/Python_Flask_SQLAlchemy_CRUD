# importing from __init__.py file
from sqlalchemycrud import db, ma

############# Customer Class/Model #############
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(255), unique=True)

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
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'))
)


############# Order Class/Model #############
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    delivery_address = db.Column(db.String(400))
    status = db.Column(db.Integer)

    # one-to-many relationship
    fk_customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))

    # many-to-many relationship
    products = db.relationship('Product', secondary = orders_products, backref = db.backref('orders', lazy =True))

    def __init__(self, delivery_address, status, fk_customer_id, customer, products):
        self.delivery_address = delivery_address
        self.status = status
        self.fk_customer_id = fk_customer_id
        self.customer = customer
        self.products = products

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'delivery_address', 'status', 'fk_customer_id')

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


############# Product Class/Model #############
class Product(db.Model):
    __tablename__ = 'products'
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

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'desc', 'price', 'qty')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)