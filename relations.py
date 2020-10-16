# relations
from sqlalchemy import ForeignKey

from database import db

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column('id', db.Integer(), primary_key = True)
    is_buyer = db.Column('is_buyer', db.Integer())
    password = db.Column('password', db.String(256))
    email = db.Column('email', db.String(256))
    question = db.Column('question', db.String(256))
    answer = db.Column('answer', db.String(256))
    address = db.Column('address', db.String(256))

class Buyer(db.Model):
    __tablename__ = 'Buyers'
    id = db.Column('id', db.Integer(), ForeignKey('Users.id'), primary_key = True)

class Seller(db.Model):
    __tablename__ = 'Sellers'
    id = db.Column('id', db.Integer(), ForeignKey('Users.id'), primary_key = True)

class Item(db.Model):
    __tablename__ = 'Items'
    sku = db.Column('SKU', db.Integer(), primary_key = True)
    title = db.Column('title', db.String(256))
    description = db.Column('description', db.String(256))
    category = db.Column('category', db.String(256))
    price = db.Column('price', db.Float())
    rating = db.Column('rating', db.Float())
    seller = db.Column('seller', db.Integer(), ForeignKey('Sellers.id'))

class Review(db.Model):
    __tablename__ = 'Reviews'
    seller_id = db.Column('seller_id', db.Integer(),  ForeignKey('Sellers.id'), primary_key = True)
    buyer_id = db.Column('buyer_id', db.Integer(),  ForeignKey('Buyers.id'), primary_key=True)
    sku = db.Column('SKU', db.Integer(), ForeignKey('Items.SUK'), primary_key = True)
    seller_rating = db.Column('seller_rating', db.Integer())
    item_rating = db.Column('item_rating', db.Integer())
    written_review = db.Column('written_review', db.String(256))

class Sells(db.Model):
    __tablename__ = 'Sells'
    seller_id = db.Column('seller_id', db.Integer(), ForeignKey('Sellers.id'), primary_key = True)
    sku = db.Column('SKU', db.Integer(), ForeignKey('Items.SKU'), primary_key = True)

class Payment(db.Model):
    __tablename__ = 'Payment'
    credit_card = db.Column('credit_card', db.Integer(), primary_key = True)
    address = db.Column('address', db.String(256))
    coupon = db.Column('coupon', db.String(256))

class PaysWith(db.Model):
    __tablename__ = 'PaysWith'
    credit_card = db.Column('credit_card', db.Integer(), ForeignKey('Payment.credit_card'), primary_key = True)
    buyer_id = db.Column('buyer_id', db.Integer(), ForeignKey('Buyers.id'))

class ItemInCategory(db.Model):
    sku = db.Column('SKU', db.Integer(), ForeignKey('Items.SKU'), primary_key = True)
    name = db.Column('name', db.Integer(), ForeignKey('Categories.name'))

class Category(db.Model):
    __tablename__ = 'Categories'
    name = db.Column('name', db.String(20), primary_key = True)

class Order(db.Model):
    __tablename__ = 'Orders'
    order_id = db.Column('order_id', db.Integer(), primary_key = True)
    total_price = db.Column('total_price', db.Float())
    time_stamp = db.Column('time_stamp', db.DateTime())

class OrdersContain(db.Model):
    __tablename__ = 'OrdersContain'
    order_id = db.Column('order_id', db.Integer(), ForeignKey('Orders.order_id'), primary_key = True)
    sku = db.Column('SKU', db.Integer(), ForeignKey('Items.SKU'), primary_key = True)
    quantity_ordered = db.Column('quantity_ordered', db.Integer())
    price_at_order = db.Column('price_at_order', db.Float())

class Places(db.Model):
    __tablename__ = 'Places'
    order_id = db.Column('order_id', db.Integer(), ForeignKey('Orders.order_id'), primary_key = True)
    buyer_id = db.Column('buyer_id', db.Integer(), ForeignKey('Buyers.id'))

class Cart(db.Model):
    __tablename__ = 'Cart'
    buyer_id = db.Column('buyer_id', db.Integer(), ForeignKey('Users.user_id'), primary_key = True)
    sku = db.Column('SKU', db.Integer(), ForeignKey('Items.SKU'), primary_key = True)

class RequiresPayment(db.Model):
    __tablename__ = 'RequiresPayment'
    order_id = db.Column('order_id', db.Integer(), ForeignKey('Orders.order_id'), primary_key = True)
    credit_card_number = db.Column('credit_card_number', db.Integer(), ForeignKey('Payment.credit_card'))

































