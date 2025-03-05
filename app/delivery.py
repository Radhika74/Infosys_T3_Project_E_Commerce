from flask import Blueprint,render_template,flash,get_flashed_messages,send_from_directory,redirect,request
from .models import Order,DeliveryPerson
from . import db

delivery_bp = Blueprint('delivery',__name__)


@delivery_bp.route('/person/<int:id>')
def dashboard(id):

    person = DeliveryPerson.query.get(id)
    available_orders = Order.query.filter_by(customer_location=person.location, delivery_person_id = None).all()

    assigned_orders = Order.query.filter_by(delivery_person_id=person.id).all()

    delivered_orders = Order.query.filter_by(delivery_status = "delivered",delivery_person_id = person.id).all()

    return render_template('delivery.html', person = person ,new_orders=available_orders, assigned_orders=assigned_orders, delivered_orders=delivered_orders)



# Assign Delivery Person

# @delivery_bp.route('/update_status', methods=['POST'])
# def update_status():
#     order_id = request.form.get('order_id')
#     delivery_person_id = request.form.get('delivery_person_id')

#     order = Order.query.get(order_id)
#     if order and delivery_person_id:
#         order.delivery_person_id = delivery_person_id
#         db.session.commit()
#         return jsonify({'message': 'Assigned successfully!'}), 200
#     return jsonify({'error': 'Invalid data'}), 400



@delivery_bp.route("/update_status/<int:order_id>/<status>", methods=['GET'])
def update_status(order_id,status):

    return f"order_id : {order_id} , ----> status : {status}"










# Update Delivery Status
@delivery_bp.route('/assign_delivery/<int:order_id>/<int:person_id>', methods=['GET','POST'])
def assign_delivery(order_id,person_id):

    try:
        order = Order.query.get(order_id)
        order.delivery_person_id = person_id

        db.session.commit()

        return redirect(f"/delivery/person/{person_id}")
    except Exception as e:
        print(f"////////////////////////////////////\n{e}")

    # order_id = request.form.get('order_id')
    # new_status = request.form.get('new_status')

    # order = Order.query.get(order_id)
    # if order:
    #     order.delivery_status = new_status
    #     if new_status == "Delivered":
    #         order.delivery_date = datetime.utcnow()
    #     db.session.commit()
    #     return jsonify({'message': 'Status updated!'}), 200
    # return jsonify({'error': 'Invalid order ID'}), 400












@delivery_bp.route("/add-delivery-persons")
def add_delivery_persons():
    
    name_ = ["naresh"]
    location_ = ["pune"]
    
    for i in range(len(name_)):
        delivery_preson = DeliveryPerson()
        delivery_preson.name = name_[i]
        delivery_preson.location = location_[i]
        db.session.add(delivery_preson)
        
    db.session.commit()
    persons = DeliveryPerson.query.order_by(DeliveryPerson.id)

    return f"{persons} added successfully to the database!!"



# @delivery_bp.route("/clear-table/<table_name>")
# def clear_table(table_name):
#     if table_name == "delivery-person" :
#         count = DeliveryPerson.query.delete()
#     elif table_name == "orders":
#         count = Order.query.delete()
#     db.session.commit()

#     return f"{count} {table_name} deleted from database"




# @delivery_bp.route("/create-orders")
# def create_orders():

#     manual_order = Order(
#         customer_name = "vishnu vardhan",
#         product_name = "watch",
#         customer_location = "hyd",
#         delivery_person_id = 1
#     )
#     db.session.add(manual_order)
#     db.session.commit()

#     # customer_name_ = ["raj","ravi","abhi","avinash","bhanu","bhavan"]
#     # product_name_ = ["phone","watch","laptop","shirt","books","bag"]
#     # # delivery_status_ = []
#     # customer_location_ = ["hyd","delhi","pune","hyd","delhi","delhi"]
#     # # delivery_person_id_ = []

#     # for i in range(len(customer_name_)):
#     #     orders = Order()
#     #     orders.customer_name = customer_name_[i]
#     #     orders.product_name = product_name_[i]
#     #     # orders.delivery_status= delivery_status_[i]
#     #     orders.customer_location = customer_location_[i]
#     #     # orders.delivery_person_id = delivery_person_id_[i]

#     #     db.session.add(orders)

#     # db.session.commit()

#     return f"{Order.query.count()} orders created"
        




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