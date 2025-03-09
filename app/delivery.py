from flask import Blueprint,render_template,flash,url_for,redirect,current_app,request
from .models import Order,DeliveryPerson,User
from . import db
from datetime import datetime
from flask_mail import Message # type: ignore
from . import mail
import smtplib


delivery_bp = Blueprint('delivery',__name__)



def send_email(user,order,token):
    """Send a Product rating email to the user"""

    print("send_email function called")

    rating_url = url_for('delivery.product_rating', token=token, _external=True)
    subject='Rate the Product'
    msg = Message(subject,sender = "vishnujavvaji19@gmail.com",recipients=["vishnujavvaji19@gmail.com"])
    msg.body = f"Hello {user.name}, \n\nYour order : {order.product_name} with ID {order.id} has been successfully delivered. Thank you for choosing us!\n\nBest regards,\nYour Delivery Team\n\nTo rate the delivered products click : {rating_url}"
    try:
        mail.send(msg)
        print(rating_url)
        print(user.email)
        
        print("Email sent")
    except smtplib.SMTPException as e:
        print(f"except smtplib.SMTPException as e: {e}")
    except Exception as e:
        print(e)
        flash("Mail not sent!!","danger")


@delivery_bp.route("/product-rating/<token>", methods=["GET", "POST"])
def product_rating(token):
    # Verify the token
    user = User.verify_reset_token(token, current_app.config['SECRET_KEY'])
    
    if not user:
        flash("Invalid or expired rating token. Please try again.", "danger")
        return "pleace retry", 404
    
    if request.method == "POST":

        return render_template("product_rating.html")

    
    return render_template("product_rating.html",user_token=token)


@delivery_bp.route('/dashboard/<int:id>')
def dashboard(id):

    person = DeliveryPerson.query.get(id)
    available_orders = Order.query.filter_by(customer_location=person.location,delivery_person_id = None).all()

    # assigned_orders = Order.query.filter_by(delivery_person_id=person.id ).all()

    delivered_orders = Order.query.filter_by(delivery_status = "Delivered",delivery_person_id = person.id).all()
    assigned_orders = Order.query.filter(Order.delivery_person_id == person.id,Order.delivery_status != "Delivered").all()


    return render_template('delivery.html', person = person ,new_orders=available_orders, assigned_orders=assigned_orders, delivered=delivered_orders)



@delivery_bp.route("/update_status/<int:order_id>/<status>", methods=['GET','POST'])
def update_status(order_id,status):

    order = Order.query.get(order_id)
    if order :

        order.delivery_status = status
        if status == "Delivered":
            order.delivery_date = datetime.now()
            user = User.query.filter_by(email=order.customer_email).first()

            # user = User.query.first()
            print(user)
            # user = User(name = order.customer_name,phone = 9505358105, email = order.customer_email,password="Vishnu@19",address="hyd",state="Telangana",city="hyd",pincode=500014)
            # db.session.add(user)
            # db.session.commit()
            token = user.generate_reset_token(current_app.config['SECRET_KEY'])
            send_email(user,order,token)
        db.session.commit()
        return redirect(f'/delivery/dashboard/{order.delivery_person_id}')
    else:
        return "no order exist", 400


@delivery_bp.route('/assign_delivery/<int:order_id>/<int:person_id>', methods=['GET','POST'])
def assign_delivery(order_id,person_id):

    try:
        order = Order.query.get(order_id)
        person = DeliveryPerson.query.get(person_id)
        if order and person:
            order.delivery_person_id = person_id

            db.session.commit()
            flash(f"you are assigned to {order.customer_name}'s product : {order.product_name} Delivery","success")

            return redirect(f"/delivery/dashboard/{person_id}")
        else:
            return "order not exist", 400
    except Exception as e:
        print(f"////////////////////////////////////\n{e}")
        return f"{e}",400




#           \\\\\\\\\\\\\\\\        radhika         //////////////////


# def send_delivery_email(user_email, order_id):
#     """Send an email notification when the order is delivered."""
#     subject = "Your Order Has Been Delivered!"
#     body = f"Hello, \n\nYour order with ID {order_id} has been successfully delivered. Thank you for choosing us!\n\nBest regards,\nYour Delivery Team"
 
#     msg = Message(subject, sender="vishnujavvaji19@gmail.com", recipients=[user_email])
#     msg.body = body
#     try:

#         mail.send(msg)
#         print(f"Email sent to {user_email} for order {order_id}")
#     except Exception as e:
#         print(f"Error sending email: {e}")








# @delivery_bp.route("/add-delivery-persons")
# def add_delivery_persons():
    
#     name_ = ["naresh"]
#     location_ = ["pune"]
    
#     for i in range(len(name_)):
#         delivery_preson = DeliveryPerson()
#         delivery_preson.name = name_[i]
#         delivery_preson.location = location_[i]
#         db.session.add(delivery_preson)
        
#     db.session.commit()
#     persons = DeliveryPerson.query.order_by(DeliveryPerson.id)

#     return f"{persons} added successfully to the database!!"



# @delivery_bp.route("/clear-table/<table_name>")
# def clear_table(table_name):
#     if table_name == "delivery-person" :
#         count = DeliveryPerson.query.delete()
#     elif table_name == "orders":
#         count = Order.query.delete()
#     db.session.commit()

#     return f"{count} {table_name} deleted from database"




@delivery_bp.route("/create-orders")
def create_orders():

    # manual_order = Order(
    #     customer_name = "vishnu vardhan",
    #     product_name = "watch",
    #     customer_location = "hyd",
    #     delivery_person_id = 1
    # )
    # db.session.add(manual_order)
    # db.session.commit()

    customer_name_ = ["raj","ravi","abhi","avinash","bhanu","bhavan","vishnu","vardhan","guptha"]
    product_name_ = ["phone","watch","laptop","shirt","books","bag","phone","book","watch"]
    # delivery_status_ = []
    customer_location_ = ["hyd","delhi","pune","hyd","delhi","delhi","pune","delhi","pune"]
    # delivery_person_id_ = []
    customer_email_ = ["vishnujavvaji19@gmail.com"]

    for i in range(len(customer_name_)):
        orders = Order()
        orders.customer_name = customer_name_[i]
        orders.product_name = product_name_[i]
        # orders.delivery_status= delivery_status_[i]
        orders.customer_location = customer_location_[i]
        orders.customer_email = customer_email_[0]
        # orders.delivery_person_id = delivery_person_id_[i]

        db.session.add(orders)

    db.session.commit()

    return f"{Order.query.count()} orders created"
        




# # @delivery_bp.route("/dashboard/<int:id>")
# # def dashboard(id):

# #     person = DeliveryPerson.query.get(id)
# #     available_orders = Order.query.filter_by(customer_location=person.location).all()

# #     print("\n\n")
# #     orders = []
# #     for order in available_orders:
# #         print(order.product_name)
# #         orders.append(order.product_name)

# #         # ///////////////       after hiting the asign me button        \\\\\\\\\\\\\\\
    
# #     # assigned_orders = Order.query.filter_by(delivery_person_id=person.id).all()
    
# #     # persons_ = []
# #     # for order in assigned_orders:
# #     #     id_=order.delivery_person_id
# #     #     print(id_)
# #     #     person_=DeliveryPerson.query.get(id_)
# #     #     print(person_)
# #     #     persons_.append(person_.name)


# #     # return f"{persons_}----------{len(assigned_orders)}------{person.name}, from {person.location}\n Avaliable orders : {orders}"

# #     # assigned_orders_ = person.orders

# #     # product_names = []
# #     # for order in assigned_orders_:
# #     #     print(order.product_name)
# #     #     product_names.append(order.product_name)


# #     # return f" assigned products are : {product_names}"
    
    

# #     # /////////////////     delivered orders        \\\\\\\\\\\\\\\\\\


# #     In_Transit_orders = Order.query.filter_by(delivery_status = "In Transit",delivery_person_id = person.id).all()
# #     delivered_orders = Order.query.filter_by(delivery_status = "delivered",delivery_person_id = person.id).all()
# #     pending_orders = Order.query.filter_by(delivery_status = "pending",delivery_person_id = person.id).all()
# #     failed_orders = Order.query.filter_by(delivery_status = "failed",delivery_person_id = person.id).all()

# #     # orders_ = Order.query.all()
# #     # for order in orders_:
# #     #     if order.delivery_person_id == 1 :
# #     #         print(order.id, order.delivery_status, order.customer_name)  # Print status of each order

# #     produsts = []
# #     for order in In_Transit_orders:
# #         # if order.delivery_person_id == 1:
# #             produsts.append(order.product_name)

# #     return f"{In_Transit_orders}-------------------{produsts}-----------len : {len(In_Transit_orders)}"




# @delivery_bp.route("/rollback")
# def rollback():
#     db.session.rollback()
#     db.session.close()

#     return f"rollback"


@delivery_bp.route("/send-mail")
def send_mail():
    if request.method == "GET" :
        msg = Message("Test Subject", sender='vishnujavvaji19@gmail.com',recipients=['rishithabhatt21@gmail.com'])
        msg.body = "Test email from Flask"
        mail.send(msg)
        print("Email Sent")

        return "check your inbox"
