from flask import Blueprint,render_template,flash,get_flashed_messages,send_from_directory,redirect,request
from .models import Order,DeliveryPerson
from . import db

delivery_bp = Blueprint('delivery',__name__)


@delivery_bp.route("/add-delivery-persons")
def add_delivery_persons():
    
    name_ = ["vishnu","nitin","rishi"]
    location_ = ["hyd","delhi","hyd"]
    
    for i in range(len(name_)):
        delivery_preson = DeliveryPerson()
        delivery_preson.name = name_[i]
        delivery_preson.location = location_[i]
        db.session.add(delivery_preson)
        
    db.session.commit()
    persons = DeliveryPerson.query.order_by(DeliveryPerson.id)

    return f"{persons} added successfully to the database!!"



@delivery_bp.route("/clear-table/<table_name>")
def clear_table(table_name):
    if table_name == "delivery-person" :
        count = DeliveryPerson.query.delete()
    elif table_name == "orders":
        count = Order.query.delete()
    db.session.commit()

    return f"{count} {table_name} deleted from database"




@delivery_bp.route("/create-orders")
def create_orders():

    customer_name_ = ["raj","ravi","abhi","avinash","bhanu","bhavan"]
    product_name_ = ["phone","watch","laptop","shirt","books","bag"]
    # delivery_status_ = []
    customer_location_ = ["hyd","delhi","pune","hyd","delhi","delhi"]
    # delivery_person_id_ = []

    for i in range(len(customer_name_)):
        orders = Order()
        orders.customer_name = customer_name_[i]
        orders.product_name = product_name_[i]
        # orders.delivery_status= delivery_status_[i]
        orders.customer_location = customer_location_[i]
        # orders.delivery_person_id = delivery_person_id_[i]

        db.session.add(orders)

    db.session.commit()

    return f"{Order.query.count()} orders created"
        

