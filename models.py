from extensions import db
from sqlalchemy import func


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), default='')
    store = db.Column(db.String(50), default='')
    category = db.Column(db.String(50), default='')
    gluten = db.Column(db.Boolean, default=False)
    in_list = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, default=0.0)
    updated = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Product {self.name}>'


class GroceryList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('grocery', lazy=True))
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float)

    def __repr__(self):
        return f'<GroceryList {self.product_id}>'


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    products = db.Column(db.String(), default='')
    description = db.Column(db.String(), default='')

    def __repr__(self):
        return f'<Recipe {self.name}>'
