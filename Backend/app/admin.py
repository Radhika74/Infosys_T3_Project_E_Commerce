from flask import Blueprint,render_template,flash,get_flashed_messages,send_from_directory,redirect
from .forms import ProductForm
from .models import Product
from . import db
from . import csrf


admin_bp = Blueprint('admin',__name__)


from flask_wtf.csrf import CSRFError

@admin_bp.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400



@admin_bp.route('/')

def profile():
    
    return render_template("admin.html")

@admin_bp.route('/cart')

def cart_page():
    
    return render_template("cart.html")



@admin_bp.route('/view-products')

def view_products():
    items = Product.query.order_by(Product.id)

    return render_template("view_products.html", items=items)




@admin_bp.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory("../media",filename)





@admin_bp.route('/add-product', methods = ['GET','POST'])
# @csrf.exempt
def add_products():

    form = ProductForm()
    if form.validate_on_submit():
        product_name = form.product_name.data
        current_price = form.current_price.data
        previous_price = form.previous_price.data
        description = form.description.data
        category = form.category.data
        in_stock = form.in_stock.data
        sale = form.sale.data

        file = form.product_picture.data
        # file_path = fr"C:\Documents sys\E-Commerce\media\{file}"
        file_path = f"./media/{file.filename}"

        file.save(file_path)
        

        new_product = Product()
        new_product.product_name = product_name
        new_product.current_price = current_price
        new_product.previous_price = previous_price
        new_product.description = description
        new_product.category = category
        new_product.in_stock = in_stock
        new_product.sale = sale

        new_product.product_picture = file_path

        try:
            db.session.add(new_product)
            db.session.commit()
            flash(f"{product_name} added successfully")
            print("product added without any errors!!")
            return render_template("add_products.html", form=form)
        except Exception as e:
            print(e)
            flash("Product Not Added!! There might be some issue!!")

        return render_template("add_products.html",form=form)

    return render_template("add_products.html", form=form)



@admin_bp.route("/clear-products-table")
def clear_table():
    table = Product()
    rows = table.query.delete()
    db.session.commit()
    flash(f" {rows} rows deleted ")
    return redirect("/admin/")
