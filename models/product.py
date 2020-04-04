from shared.database import db, ma


class Product(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), unique=True)
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


# Always use "strict=True" to avoid errors
product_schema = ProductSchema(strict=True)
# For many products manipulation
products_schema = ProductSchema(many=True, strict=True)
