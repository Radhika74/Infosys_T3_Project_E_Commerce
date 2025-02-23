from app import db
from app.models import Product
from bs4 import BeautifulSoup 
import io



def get_csrf_token(client, url):
    response = client.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    csrf_exist = soup.find('input', {'name': 'csrf_token'})
    if csrf_exist:
        return csrf_exist['value']
    else:
        raise ValueError(f' CSRF token is missing in the given path {url}')




def test_add_product(client,app):
    with app.app_context():
        initial_count = Product.query.count()

    csrf_token = get_csrf_token(client, '/admin/add-product')
    dummy_file = (io.BytesIO(b'test file content'),"test_image.png")
    response = client.post('/admin/add-product', data={
        'csrf_token' : csrf_token,
        'product_name': 'New Test Product',
        'current_price': 99.99,
        'previous_price': 120.00,
        'description': 'A sample product',
        'category': 'Fashion',
        'quantity': 10,
        # uncomment while executing this test, i commented because to check whether the test is working if i not provide the followling fields
        # 'size_small': 5,
        # 'size_medium': 3,
        # 'size_large': 2,
        'sale': True,
        'product_picture' : dummy_file
        },content_type = 'multipart/form-data',follow_redirects=True)

    assert b"added successfully" in response.data
    assert response.status_code == 200
    with app.app_context():
        current_count = Product.query.count()
        assert current_count == initial_count + 1




def test_update_product(client,app):
    with app.app_context():
        product = Product.query.first()
        before_update = db.session.get(Product,product.id)
        print(f"Before Update: {before_update.current_price}")
        assert product is not None

    csrf_token = get_csrf_token(client, f'/admin/update-item/{product.id}' )    

    dummy_file = (io.BytesIO(b"test file content"),"test_image.png")


    response = client.post(f'/admin/update-item/{product.id}', data={
    'csrf_token': csrf_token,  
    'product_name': 'test by vishnu',
    'current_price': 800.00,  
    'previous_price': product.previous_price,
    'description': product.description,
    'category': product.category,
    'quantity': product.quantity,
    'size_small': product.size_small,
    'size_medium': product.size_medium,
    'size_large': product.size_large,
    'sale': product.sale,
    'product_picture' : dummy_file
    }, content_type='multipart/form-data',follow_redirects=True)

    assert response.status_code == 200


    with app.app_context():
        updated_product = db.session.get(Product,product.id)
        print(f"After Update: {updated_product.current_price}")
        assert updated_product.product_name == 'test by vishnu'
        assert updated_product.current_price == 800.00




# Run delete after once executing this file, because i'm using the first product for both Update and Delete testing
# before running Delete comment Update.
# the CRUD testing completed yaay!!



# def test_delete_product(client,app):
#     with app.app_context():

#         initial_count = Product.query.count()
#         product = Product.query.first()
       
#         # product_id = product.id
#         product_id = 20     # check before running
    
#     response = client.get(f"/admin/delete-item/{product_id}")
#     assert response.status_code == 302  
#     with client.application.app_context():
#         deleted_product = db.session.get(Product, product_id)
#         assert Product.query.count() == initial_count - 1 
#         assert deleted_product is None

