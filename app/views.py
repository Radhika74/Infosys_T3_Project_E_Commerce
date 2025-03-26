from flask import Blueprint, flash, redirect,render_template, request, url_for,send_from_directory
from .models import Product
from . import db

views_bp = Blueprint('views',__name__)

@views_bp.route('/')

def index():
    products = Product.query.all()
    # print("\n\n")
    # print(products)
    # return render_template("home.html",items=products)
    return "Views page"


@views_bp.route('/customer_review/<int:product_id>/<token>', methods=['GET', 'POST'])
def customer_review(product_id,token):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST'and token:
        try:
            # Get the rating from the form submission and convert it to an integer
            rating = int(request.form.get('rating', 0))
        except ValueError:
            flash("Invalid rating value.", "danger")
            return redirect(url_for('views_bp.customer_review', product_id=product_id))
        
        # Enforce a valid rating range (e.g., 1-5 stars)
        if rating < 1 or rating > 5:
            flash("Rating must be between 1 and 5.", "danger")
            return redirect(url_for('views_bp.customer_review', product_id=product_id))
        
        # If the product already has a rating, calculate the new average rating.
        if product.rating > 0:
            # This calculates a simple average between the old rating and the new one.
            # Note: For a more accurate average when multiple reviews exist, consider storing a review count.
            product.rating = round((product.rating + rating) / 2.0, 1)
        else:
            product.rating = rating
        
        db.session.commit()
        flash("Customer Review Successful!", "success")
        
        # Redirect to a product detail page or another page as needed
        return """
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    text-align: center;
                    padding: 50px;
                }
                .message-container {
                    max-width: 400px;
                    margin: auto;
                    background: white;
                    padding: 20px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                    border-radius: 8px;
                }
                .success-message {
                    background-color: #dabdab;
                    color: white;
                    padding: 15px;
                    border-radius: 5px;
                    font-size: 20px;
                }
            </style>
        </head>
        <body>
            <div class='message-container'>
                <div class='success-message'>Thank you for your review!</div>
            </div>
        </body>
        </html>
        """
    
    return render_template('customer_review.html', product=product,token=token)
