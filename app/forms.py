from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange, optional
from flask_wtf.file import FileField

class ProductForm(FlaskForm):
    product_name = StringField(label="Product Name",validators = [DataRequired()])
    product_picture = FileField(label='Product Picture', validators=[DataRequired()])
    current_price = FloatField(label='Current Price', validators=[DataRequired()])
    previous_price = FloatField(label='Previous Price', validators=[DataRequired()])
    description = StringField(label="Description of the product",validators = [DataRequired()])
    category = StringField(label="Product Category",validators = [DataRequired()])
    quantity = IntegerField(label='Quantity', validators=[optional(),NumberRange(min=0)])
    size_small = IntegerField(label='Small Quantity', validators=[optional(),NumberRange(min=0)] )
    size_medium = IntegerField(label='Medium Quantity', validators=[optional(),NumberRange(min=0)] )
    size_large = IntegerField(label='Large Quantity', validators=[optional(),NumberRange(min=0)] )
    sale = BooleanField(label='Flash Sale', default=False)

    add_product = SubmitField('Add Product')
    update_product = SubmitField('Upadte Product')

    def __repr__(self):
        return f" product form : {self.product_name}"

