from flask import Blueprint, flash, redirect,render_template, request, url_for,send_from_directory
from .models import Product,Order,User,DeliveryPerson
from . import db

views_bp = Blueprint('views',__name__)

@views_bp.route('/')

def index():
    products = Product.query.all()
    # print("\n\n")
    # print(products)
    # return render_template("home.html",items=products)
    return "Views page"


@views_bp.route('/customer_review/<int:user_id>/<int:order_id>/<token>', methods=['GET', 'POST'])
def customer_review(user_id, order_id, token):
    user = User.query.get_or_404(user_id)
    order = Order.query.get_or_404(order_id)
    product = Product.query.get_or_404(order.product_id)

    if request.method == 'POST' and token:
        try:
            rating = int(request.form.get('rating', 0))
        except ValueError:
            flash("Invalid rating value.", "danger")
            return redirect(url_for('views.customer_review', user_id=user_id, order_id=order_id, token=token))

        if rating < 1 or rating > 5:
            flash("Rating must be between 1 and 5.", "danger")
            return redirect(url_for('views.customer_review', user_id=user_id, order_id=order_id, token=token))

        if product.rating > 0:
            product.rating = round((product.rating + rating) / 2.0, 1)
        else:
            product.rating = rating

        order.has_rated = True
        db.session.commit()
        flash("Customer Review Successful!", "success")

        return redirect(url_for('views.customer_review', user_id=user_id, order_id=order_id, token=token))

    return render_template('customer_review.html', user=user, order=order, token=token)




# @views_bp.route('/customer_review/<int:user_id>/<int:product_id>/<int:order_id>/<token>', methods=['GET', 'POST'])
# def customer_review(user_id, product_id, order_id, token):
#     user = User.query.get_or_404(user_id)
#     product = Product.query.get_or_404(product_id)
#     order = Order.query.get_or_404(order_id)

#     if request.method == 'POST' and token:
#         try:
#             rating = int(request.form.get('rating', 0))
#         except ValueError:
#             flash("Invalid rating value.", "danger")
#             return redirect(url_for('views_bp.customer_review', user_id=user_id, product_id=product_id, order_id=order_id, token=token))

#         if rating < 1 or rating > 5:
#             flash("Rating must be between 1 and 5.", "danger")
#             return redirect(url_for('views_bp.customer_review', user_id=user_id, product_id=product_id, order_id=order_id, token=token))

#         if product.rating > 0:
#             product.rating = round((product.rating + rating) / 2.0, 1)
#         else:
#             product.rating = rating

#         order.has_rated = True # Update the order table.
#         db.session.commit()
#         flash("Customer Review Successful!", "success")

#         return """
#         <html>
#         <head>
#             <style>
#                 body {
#                     font-family: Arial, sans-serif;
#                     background-color: #f4f4f4;
#                     text-align: center;
#                     padding: 50px;
#                 }
#                 .message-container {
#                     max-width: 400px;
#                     margin: auto;
#                     background: white;
#                     padding: 20px;
#                     box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
#                     border-radius: 8px;
#                 }
#                 .success-message {
#                     background-color: #dabdab;
#                     color: white;
#                     padding: 15px;
#                     border-radius: 5px;
#                     font-size: 20px;
#                 }
#             </style>
#         </head>
#         <body>
#             <div class='message-container'>
#                 <div class='success-message'>Thank you for your review!</div>
#             </div>
#         </body>
#         </html>
#         """

#     return render_template('customer_review.html', user=user, product=product, token=token)

# @views_bp.route('/customer_review/<int:user_id>/<int:product_id>/<token>', methods=['GET', 'POST'])
# def customer_review(user_id,product_id,token):
#     user = User.query.get_or_404(user_id)
    
#     product = Product.query.get_or_404(product_id)
#     if request.method == 'POST'and token:
#         try:
#             # Get the rating from the form submission and convert it to an integer
#             rating = int(request.form.get('rating', 0))
#         except ValueError:
#             flash("Invalid rating value.", "danger")
#             return redirect(url_for('views_bp.customer_review', product_id=product_id))
        
#         # Enforce a valid rating range (e.g., 1-5 stars)
#         if rating < 1 or rating > 5:
#             flash("Rating must be between 1 and 5.", "danger")
#             return redirect(url_for('views_bp.customer_review', product_id=product_id))
        
#         # If the product already has a rating, calculate the new average rating.
#         if product.rating > 0:
#             # This calculates a simple average between the old rating and the new one.
#             # Note: For a more accurate average when multiple reviews exist, consider storing a review count.
#             product.rating = round((product.rating + rating) / 2.0, 1)
#         else:
#             product.rating = rating
        
#         db.session.commit()
#         flash("Customer Review Successful!", "success")
        
#         # Redirect to a product detail page or another page as needed
#         return """
#         <html>
#         <head>
#             <style>
#                 body {
#                     font-family: Arial, sans-serif;
#                     background-color: #f4f4f4;
#                     text-align: center;
#                     padding: 50px;
#                 }
#                 .message-container {
#                     max-width: 400px;
#                     margin: auto;
#                     background: white;
#                     padding: 20px;
#                     box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
#                     border-radius: 8px;
#                 }
#                 .success-message {
#                     background-color: #dabdab;
#                     color: white;
#                     padding: 15px;
#                     border-radius: 5px;
#                     font-size: 20px;
#                 }
#             </style>
#         </head>
#         <body>
#             <div class='message-container'>
#                 <div class='success-message'>Thank you for your review!</div>
#             </div>
#         </body>
#         </html>
#         """
    
#     return render_template('customer_review.html',user = user, product=product,token=token)


@views_bp.route("/create-data")
def create_data():
    # user = User(
    #     name = "vishnu",
    #     phone = "9505358105",
    #     email = "vishnujavvaji19@gmail.com",
    #     password = "Vishnu@19",
    #     address = "1-1/1",
    #     state = "Telangana",
    #     city = "hyd",
    #     pincode = "500014"
    # )

    user = User.query.order_by(User.id).first_or_404()

    # DPerson = DeliveryPerson(
    #     name = "VishnuVardhan",
    #     location = "hyd"
    # )

    DPerson = DeliveryPerson.query.order_by(DeliveryPerson.id).first_or_404()

    # db.session.add_all([user,DPerson])
    # db.session.commit()

    products = Product.query.order_by(Product.id)
    
    # for product in products:
    #     order = Order()
    #     order.product_id = product.id
    #     order.customer_id = user.id
    #     order.delivery_person_id = DPerson.id
    #     order.customer_name = user.name
    #     order.product_name = product.product_name
    #     order.customer_location = user.city
    #     order.customer_email = user.email
    #     order.customer_address = user.address

    #     db.session.add(order)
    # db.session.commit()

    # orders = Order.query.order_by(Order.id)

    user_orders = user.orders
    
    return render_template("data.html", orders = user_orders) 

    