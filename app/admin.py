from flask import Blueprint,render_template,flash,get_flashed_messages,send_from_directory,redirect,request
from .forms import ProductForm
from .models import Product,ProductSize
from . import db
from . import csrf


admin_bp = Blueprint('admin',__name__)


from flask_wtf.csrf import CSRFError

@admin_bp.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400



@admin_bp.route('/')

def profile():

    products = Product.query.order_by(Product.id)
    return render_template("admin.html", items = products)



@admin_bp.route('/cart')

def cart_page():
    
    return render_template("cart.html")



@admin_bp.route('/view-products')

def view_products():
    products = Product.query.order_by(Product.id)
    print(f" products : {products}")

    return render_template("view_products.html", items=products)




@admin_bp.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory("../media",filename)





@admin_bp.route('/add-product', methods = ['GET','POST'])
# @csrf.exempt
def add_products():

    form = ProductForm()
    if request.method == "GET":
        form.sizes.entries = []  # Remove any default entries
        form.sizes.append_entry()  # Add only one entry

    print(f"Before validation: {len(form.sizes.entries)}")  # Before validation

    if form.validate_on_submit():

        # print(f" Form Data : {request.form}") #for testing
        print(f"After validation: {len(form.sizes.entries)}")  # After validation


        product_name = form.product_name.data
        current_price = form.current_price.data
        previous_price = form.previous_price.data
        description = form.description.data
        category = form.category.data
        sale = form.sale.data

        file = form.product_picture.data
        print(f"//////////////////////////////////////////////////////////////////\nfile : {file}")
        # file_path = fr"C:\Documents sys\E-Commerce\media\{file}"
        print(f"//////////////////////////////////////////////////////////////////\nfile.filename : {file.filename}")
        file_path = f"./media/{file.filename}"
        print(f"//////////////////////////////////////////////////////////////////\nfile_path : {file_path}")

        file.save(file_path)
        

        new_product = Product()
        new_product.product_name = product_name
        new_product.current_price = current_price
        new_product.previous_price = previous_price
        new_product.description = description
        new_product.category = category
        new_product.sale = sale

        new_product.product_picture = file_path

        try:
            db.session.add(new_product)
            db.session.commit()

            print("\n\n")
            print(len(form.sizes.entries))

            for size_form in form.sizes.data:  # Correctly iterating over form data
                new_size = ProductSize(
                    product_id=new_product.id,
                    size=size_form["size"],
                    quantity=size_form["quantity"]
                )
                db.session.add(new_size)
            
            db.session.commit()
            
            flash(f"{product_name} added successfully","success")
            print("product added without any errors!!")
            return redirect("/admin/add-product")
            # return render_template("add_products.html", form=form)
        except Exception as e:
            print(e)
            flash("Product Not Added!! There might be some issue!!", "danger")

    return render_template("add_products.html", form=form)



@admin_bp.route("/clear-products-table")
def clear_table():
    table = Product()
    rows = table.query.delete()
    db.session.commit()
    flash(f" Removed all Products\n Number of products deleted : {rows} ", "danger")
    return redirect("/admin/")


@admin_bp.route("/delete-item/<id>", methods= ['GET','POST'] )

def delete_item(id):
    
    try:
        item_to_delete = Product.query.get(id)
        db.session.delete(item_to_delete)
        db.session.commit()
        flash(f'{item_to_delete.product_name} deleted',"success")
        return redirect('/admin/view-products')
    except Exception as e:
        print('Item not deleted', e)
        flash('Item not deleted!!', "danger")
    return redirect('/admin/view-products')




# @admin_bp.route("/update-item/<id>", methods= ['GET','POST'] )

# def update_item(id):
#     item_to_update = Product.query.get(id)
#     form = ProductForm(obj=item_to_update)

#     form.product_name.render_kw = {'placeholder': item_to_update.product_name}
#     form.current_price.render_kw = {'placeholder': item_to_update.current_price}
#     form.previous_price.render_kw = {'placeholder': item_to_update.previous_price}
#     form.description.render_kw = {'placeholder': item_to_update.description}
#     form.category.render_kw = {'placeholder': item_to_update.category}
#     form.quantity.render_kw = {'placeholder': item_to_update.quantity}
#     form.size_small.render_kw = {'placeholder': item_to_update.size_small}
#     form.size_medium.render_kw = {'placeholder': item_to_update.size_medium}
#     form.size_large.render_kw = {'placeholder': item_to_update.size_large}
    
#     if form.validate_on_submit():

#         print(f" Form Data : {request.form}") #for testing

#         print(f" form validated of product id : {item_to_update.id}")  # for testing
#         product_name = form.product_name.data
#         current_price = form.current_price.data
#         previous_price = form.previous_price.data
#         description = form.description.data
#         category = form.category.data
#         quantity = form.quantity.data
#         size_small = form.size_small.data
#         size_medium = form.size_medium.data
#         size_large = form.size_large.data
#         sale = form.sale.data

#         file = form.product_picture.data
#         file_path = f"./media/{file.filename}"

#         file.save(file_path)

#         try:
#             Product.query.filter_by(id=id).update(dict(
#                 product_name = product_name,
#                 current_price = current_price,
#                 previous_price = previous_price,
#                 description = description,
#                 category = category,
#                 quantity = quantity,
#                 size_small = size_small,
#                 size_medium = size_medium,
#                 size_large = size_large,
#                 sale = sale,
#                 product_picture = file_path
#             ))
#             db.session.commit()
#             flash(f'{product_name} updated Successfully',"success")
#             print('Product Upadted')
#             return redirect('/admin/view-products')
            
#         except Exception as e:
#             print('Product not Upated', e)
#             flash('Item Not Updated!!!', "danger")
            
#     return render_template("update_item.html", form=form)