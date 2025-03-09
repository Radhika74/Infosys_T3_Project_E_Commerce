from flask import Blueprint
from flask_mail import Message


views_bp = Blueprint('views',__name__)

@views_bp.route('/')

def index():

    

    return "Views page"