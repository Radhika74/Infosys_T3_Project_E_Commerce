from . import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_picture = db.Column(db.String(1000), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    previous_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(2000), default = product_name)
    color = db.Column(db.String(15))
    rating = db.Column(db.Integer, default = 0)
    category = db.Column(db.String(30))
    quantity = db.Column(db.Integer,default=0)
    sale = db.Column(db.Boolean, default=True)
    size_small = db.Column(db.Integer,default=0)
    size_medium = db.Column(db.Integer,default=0)
    size_large = db.Column(db.Integer,default=0)
    # print(f"{__table__}")


    def __repr__(self):
        return f" product name : {self.product_name}"