from . import db
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature



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
    sale = db.Column(db.Boolean, default=False)
    discount = db.Column(db.Integer,nullable=True)
    quantity_size = db.relationship('ProductSize',backref = 'product',lazy = True)


    def __repr__(self):
        return f" product name : {self.product_name}"
    

class DeliveryPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(20), nullable=False)
    orders = db.relationship('Order', backref='delivery_person', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(30), nullable=False)
    product_name = db.Column(db.String(30), nullable=False)
    delivery_status = db.Column(db.String(20), nullable=False, default='In Transit')
    customer_location = db.Column(db.String(20), nullable=False)
    order_date = db.Column(db.DateTime(), nullable=True, default=lambda: datetime.now())
    delivery_date = db.Column(db.DateTime(), nullable=True)
    customer_email = db.Column(db.String(50),nullable=False)
    delivery_person_id = db.Column(db.Integer, db.ForeignKey('delivery_person.id'), nullable=True)


class ProductSize(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    size = db.Column(db.String(50), nullable=False, default="No size")
    quantity = db.Column(db.Integer, nullable=False, default = 0)
    




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    
    def generate_reset_token(self, secret_key):
        """Generate a unique reset token for password reset"""
        serializer = URLSafeTimedSerializer(secret_key)
        self.reset_token = serializer.dumps(self.email, salt='password-reset-salt')
        self.reset_token_expiry = datetime.now() + timedelta(hours=1)  # Token expires in 1 hour
        db.session.commit()
        return self.reset_token
    
    @staticmethod
    def verify_reset_token(token, secret_key):
        """Verify a reset token and return the user if valid"""
        serializer = URLSafeTimedSerializer(secret_key)
        try:
            email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # 1 hour expiry
            return User.query.filter_by(email=email).first()
        except (SignatureExpired, BadSignature):
            return print("SignatureExpired : ",SignatureExpired , "BadSignature : ",BadSignature)
