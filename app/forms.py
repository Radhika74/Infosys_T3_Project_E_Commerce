from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, BooleanField, SubmitField,FormField, FieldList
from wtforms.validators import DataRequired, NumberRange, optional
from flask_wtf.file import FileField



class SizeQuantityForm(FlaskForm):
    size = StringField(label="Size", validators=[DataRequired()])
    quantity = IntegerField(label="Quantity", validators=[DataRequired(), NumberRange(min=0)])




class ProductForm(FlaskForm):
    product_name = StringField(label="Product Name",validators = [DataRequired()])
    product_picture = FileField(label='Product Picture', validators=[DataRequired()])
    current_price = FloatField(label='Current Price', validators=[DataRequired()])
    previous_price = FloatField(label='Previous Price', validators=[DataRequired()])
    description = StringField(label="Description of the product",validators = [DataRequired()])
    category = StringField(label="Product Category",validators = [DataRequired()])
    sale = BooleanField(label='Flash Sale', default=False)


    sizes = FieldList(FormField(SizeQuantityForm),min_entries=1)
    add_product = SubmitField('Add Product')
    update_product = SubmitField('Update Product')

    def __repr__(self):
        return f" product form : {self.product_name}"
    

