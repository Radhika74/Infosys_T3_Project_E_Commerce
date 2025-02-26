from flask import Blueprint,render_template
from .models import Product

views_bp = Blueprint('views',__name__)

@views_bp.route('/')

def index():
    products = Product.query.all()
    # print("\n\n")
    # print(products)
    return render_template("home.html",items=products)