from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField

class ProductForm(FlaskForm):
    product_name = StringField(label="Name of the product",validators = [DataRequired()])
    product_picture = FileField(label='Product Picture', validators=[DataRequired()])
    current_price = FloatField(label='Current Price', validators=[DataRequired()])
    previous_price = FloatField(label='Previous Price', validators=[DataRequired()])
    description = StringField(label="Description of the product",validators = [DataRequired()])
    category = StringField(label="Product Category",validators = [DataRequired()])
    in_stock = IntegerField(label='In Stock', validators=[DataRequired(), NumberRange(min=0)])
    sale = BooleanField(label='Flash Sale', default=False)
    add_product = SubmitField('Add Product')

    def __repr__(self):
        return f" product form : {self.product_name}"

