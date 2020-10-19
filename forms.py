from flask_wtf import FlaskForm
from wtforms import StringField, TextField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired


class AddItemForm(FlaskForm):
    """Form to add a new item to the database"""
    sku = IntegerField('sku', [DataRequired()])
    title = TextField('title', [DataRequired()])
    description = TextField('description', [DataRequired()])
    category = StringField('category', [DataRequired()])
    quantity = IntegerField('quantity', [DataRequired()])
    price = DecimalField('price', [DataRequired()], places=2)
    seller = IntegerField('seller', [DataRequired()])
    image = StringField('image')
    submit = SubmitField('Submit')
