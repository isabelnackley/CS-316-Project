from flask_wtf import FlaskForm
from wtforms import StringField, TextField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired


class AddItemForm(FlaskForm):
    """Form to add a new item to the database"""
    sku = IntegerField('SKU', [DataRequired()])
    title = TextField('Title', [DataRequired()])
    description = TextField('Description', [DataRequired()])
    category = StringField('Category', [DataRequired()])
    quantity = IntegerField('Quantity', [DataRequired()])
    price = DecimalField('Price', [DataRequired()], places=2)
    seller = IntegerField('Seller', [DataRequired()])
    image = StringField('Image')
    submit = SubmitField('Submit')
