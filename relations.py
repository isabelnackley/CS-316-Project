# relations
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from database import db


class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column('id', db.Integer(), primary_key=True)
    is_seller = db.Column('is_seller', db.Integer())
    password = db.Column('password', db.String(256))
    email = db.Column('email', db.String(256))
    question = db.Column('question', db.String(256))
    answer = db.Column('answer', db.String(256))
    address = db.Column('address', db.String(256))
    @staticmethod
    def updateUser(password, email, question, answer, address, id):
        db.session.execute('UPDATE Users SET password = :password, email = :email, question = :question, answer = '
                           ':answer, address = :address WHERE id = :id',
                           {'password': password, 'email': email, 'question': question, 'answer': answer,
                            'address': address, 'id': id})
        print("User updated")
        db.session.commit()

    def __init__(self, id=None, is_buyer=None, password=None,
                 email=None, question=None, answer=None, address=None):
        self.id = id
        self.is_buyer = is_buyer
        self.password = password
        self.email = email
        self.question = question
        self.answer = answer
        self.address = address

    def __repr__(self):
        return '<User %r>' % self.model


class Buyer(db.Model):
    __tablename__ = 'Buyers'
    id = db.Column('id', db.Integer(), ForeignKey('Users.id'), primary_key=True)

    def __init__(self, id=None):
        self.id = id

    def __repr__(self):
        return '<Buyer %r' % self.model


class Seller(db.Model):
    __tablename__ = 'Sellers'
    id = db.Column('id', db.Integer(), ForeignKey('Users.id'), primary_key=True)

    def __init__(self, id=None):  # , rating = None):
        self.id = id
        # self.rating = rating

    def __repr__(self):
        return '<Seller %r' % self.model


class Item(db.Model):
    __tablename__ = 'Items'
    sku = db.Column('SKU', db.Integer(), primary_key=True)
    title = db.Column('title', db.String(256))
    description = db.Column('description', db.String(256))
    category = db.Column('category', db.String(256))
    quantity = db.column('quantity', db.Integer())
    price = db.Column('price', db.Float())
    rating = db.Column('rating', db.Float())
    seller = db.Column('seller', db.Integer(), ForeignKey('Sellers.id'))
    image = db.Column('image', db.String(256))

    @staticmethod
    def updateItem(title, description, category, quantity, price, image, sku):
        db.session.execute('UPDATE Items SET title = :title, description = :description, category = :category, quantity = '
                           ':quantity, price = :price, image = :image WHERE sku = :sku',
                           {'title': title, 'description': description, 'category': category, 'quantity': quantity,
                            'price': price, 'image': image, 'sku': sku})
        print("Item updated")
        db.session.commit()
    def __init__(self, sku=None, title=None, description=None, category=None,
                 quantity=None, price=None, rating=None, seller=None, image=None):
        self.sku = sku
        self.title = title
        self.description = description
        self.category = category
        self.quantity = quantity
        self.price = price
        self.rating = rating
        self.seller = seller
        self.image = image

    def __repr__(self):
        return '<Item %r>' % self.model


class Review(db.Model):
    __tablename__ = 'Reviews'
    seller_id = db.Column('seller_id', db.Integer(), ForeignKey('Sellers.id'), primary_key=True)
    buyer_id = db.Column('buyer_id', db.Integer(), ForeignKey('Buyers.id'), primary_key=True)
    sku = db.Column('SKU', db.Integer(), ForeignKey('Items.SUK'), primary_key=True)
    seller_rating = db.Column('seller_rating', db.Integer())
    item_rating = db.Column('item_rating', db.Integer())
    written_review = db.Column('written_review', db.String(256))

    def __init__(self, seller_id=None, buyer_id=None, sku=None, seller_rating=None,
                 item_rating=None, written_review=None):
        self.seller_id = seller_id
        self.buyer_id = buyer_id
        self.sku = sku
        self.seller_rating = seller_rating
        self.item_rating = item_rating
        self.written_review = written_review

    def __repr__(self):
        return '<Review %r>' % self.model


class Sells(db.Model):
    __tablename__ = 'Sells'
    seller_id = db.Column('seller_id', db.Integer(), ForeignKey('Sellers.id'), primary_key=True)
    sku = db.Column('SKU', db.Integer(), ForeignKey('Items.SKU'), primary_key=True)

    def __init__(self, seller_id=None, sku=None):
        self.seller_id = seller_id
        self.sku = sku

    def __repr__(self):
        return '<Sells %r>' % self.model


class Payment(db.Model):
    __tablename__ = 'Payment'
    credit_card = db.Column('credit_card', db.Integer(), primary_key=True)
    address = db.Column('address', db.String(256))
    coupon = db.Column('coupon', db.String(256))

    def __init__(self, credit_card=None, address=None, coupon=None):
        self.credit_card = credit_card
        self.address = address
        self.coupon = coupon

    def __repr__(self):
        return '<Payment %r>' % self.model


class PaysWith(db.Model):
    __tablename__ = 'PaysWith'
    credit_card = db.Column('credit_card', db.Integer(), ForeignKey('Payment.credit_card'), primary_key=True)
    buyer_id = db.Column('buyer_id', db.Integer(), ForeignKey('Buyers.id'))

    def __init__(self, credit_card=None, buyer_id=None):
        self.credit_card = credit_card
        self.buyer_id = buyer_id

    def __repr__(self):
        return '<PaysWith %r>' % self.model


class ItemInCategory(db.Model):
    sku = db.Column('SKU', db.Integer(), ForeignKey('Items.SKU'), primary_key=True)
    name = db.Column('name', db.Integer(), ForeignKey('Categories.name'))

    def __init__(self, sku=None, name=None):
        self.sku = sku
        self.name = name

    def __repr__(self):
        return '<ItemsInCategory %r>' % self.model


class Category(db.Model):
    __tablename__ = 'Categories'
    name = db.Column('name', db.String(20), primary_key=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.model


class Order(db.Model):
    __tablename__ = 'Orders'
    order_id = db.Column('order_id', db.Integer(), primary_key=True)
    total_price = db.Column('total_price', db.Float())
    time_stamp = db.Column('time_stamp', db.DateTime())
    buyer_id = db.Column('buyer_id', db.Integer())

    def __init__(self, order_id=None, total_price=None, time_stamp=None,
                 buyer_id=None):
        self.order_id = order_id
        self.total_price = total_price
        self.time_stamp = time_stamp
        self.buyer_id = buyer_id

    def __repr__(self):
        return '<Order %r>' % self.model


class OrdersContain(db.Model):
    __tablename__ = 'OrdersContain'
    order_id = db.Column('order_id', db.Integer(), ForeignKey('Orders.order_id'), primary_key=True)
    sku = db.Column('SKU', db.Integer(), ForeignKey('Items.SKU'), primary_key=True)
    quantity_ordered = db.Column('quantity_ordered', db.Integer())
    price_at_order = db.Column('price_at_order', db.Float())

    def __init__(self, order_id=None, sku=None, quantity_ordered=None, price_at_order=None):
        self.order_id = order_id
        self.sku = sku
        self.quantity_ordered = quantity_ordered
        self.price_at_order = price_at_order

    def __repr__(self):
        return '<OrdersContain %r>' % self.model


class Places(db.Model):
    __tablename__ = 'Places'
    order_id = db.Column('order_id', db.Integer(), ForeignKey('Orders.order_id'), primary_key=True)
    buyer_id = db.Column('buyer_id', db.Integer(), ForeignKey('Buyers.id'))

    def __init__(self, order_id=None, buyer_id=None):
        self.order_id = order_id
        self.buyer_id = buyer_id

    def __repr__(self):
        return '<Places %r>' % self.model


class Cart(db.Model):
    __tablename__ = 'Cart'
    buyer_id = db.Column('buyer_id', db.Integer(), primary_key=True)
    sku = db.Column('SKU', db.Integer(), primary_key=True)

    @staticmethod
    def delete_from_cart(sku, buyer_id):
        db.session.execute('DELETE FROM Cart WHERE sku = :sku AND buyer_id = :buyer_id',
                           {'sku': sku, 'buyer_id': buyer_id})
        print("Deleted from cart")
        db.session.commit()

    def __init__(self, buyer_id=None, sku=None):
        self.buyer_id = buyer_id
        self.sku = sku

    def __repr__(self):
        return '<Cart %r>' % self.model




class RequiresPayment(db.Model):
    __tablename__ = 'RequiresPayment'
    order_id = db.Column('order_id', db.Integer(), ForeignKey('Orders.order_id'), primary_key=True)
    credit_card_number = db.Column('credit_card_number', db.Integer(), ForeignKey('Payment.credit_card'))

    def __init__(self, order_id=None, credit_card_number=None):
        self.order_id = order_id
        self.credit_card_number = credit_card_number

    def __repr__(self):
        return '<RequiresPayment %r>' % self.model
