# database
from flask import Flask, render_template, redirect, url_for, jsonify, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required
import os
from sqlalchemy import or_
import pymysql
from werkzeug.datastructures import MultiDict

import relations
from forms import AddItemForm, EditProfileForm, EditItemForm, WriteReviewForm, LoginForm, ForgotPasswordForm, \
    VerifyEmailForm, SearchItemsForm

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:password@152.3.52.135/test1'

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
User = {'id': 1, 'is_seller': 0}  # dummy user who is placeholder until we make login

login_manager = LoginManager()
login_manager.init_app(app)

"""Functions for the main page"""


@app.route('/', methods=["GET", "POST"])
def main():
    result = list()
    form = SearchItemsForm()
    search_string = form.item.data
    if search_string is None:
        query = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price,
                                 relations.Item.rating, relations.Item.seller, relations.Item.image).all()
    else:
        query = db.session.query(relations.Item).filter(or_(relations.Item.title.like(f'%{search_string}%'),
                                                            relations.Item.seller.like(f'%{search_string}%'),
                                                            relations.Item.category.like(f'%{search_string}%')))

    for row in query:
        temp = {'sku': row.sku, 'title': row.title, 'category': row.category, 'price': row.price,
                'rating': row.rating, 'seller': row.seller, 'image': row.image}
        result.append(temp)

    cat_list = list()
    categories = db.session.query(relations.Item.category).distinct()
    for row in categories:
        temp = {'name': row.category}
        cat_list.append(temp)

    return render_template('index.html', items=result, form=form, categories=cat_list)


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return db.session.query(relations.User).filter_by(id=user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))
    #TODO: add flash message "You must be logged in to view that page."


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if request.method == "POST":
        user = db.session.query(relations.User).filter_by(email=form.email.data).first()
        print(form.email.data)
        if user and user.password==form.password.data:
            print(form.password.data)
            login_user(user)
            return redirect(url_for('main'))
        # TODO: add flash of incorrect username/password
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/verifyemail', methods=["GET", "POST"])
def verify_email():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = VerifyEmailForm()
    if request.method == 'POST':
        user = db.session.query(relations.User).filter_by(email=form.email.data).first()
        if user:
            return redirect(url_for('forgot_password', user=user.id))
    return render_template('verify_email.html', form=form)


@app.route('/<user>/forgotpassword', methods=["POST", "GET"])
def forgot_password(user):
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    user_object = db.session.query(relations.User).filter_by(id=user).first()
    question = user_object.question
    password= ""
    form = ForgotPasswordForm()
    if request.method == 'POST':
        if user and user_object.answer==form.answer.data:
            password= user_object.password
            return render_template('forgot_password.html', form=form, password=password, question=question)
    return render_template('forgot_password.html', form=form, password=password,  question=question)


@app.route("/category/<name>", methods=["GET", "POST"])
def category_page(name):
    items_list = list()
    items_query = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.price,
                                   relations.Item.rating, relations.Item.seller,
                                   relations.Item.image).filter(relations.Item.category == name)
    for row in items_query:
        temp = {'sku': row.sku, 'title': row.title, 'price': row.price,
                'rating': row.rating, 'seller': row.seller, 'image': row.image}
        items_list.append(temp)
    name_dict = {'name': name}
    cat_list = list()
    categories = db.session.query(relations.Item.category).distinct()
    for row in categories:
        temp = {'name': row.category}
        cat_list.append(temp)
    return render_template('category.html', items=items_list, name=name_dict, categories=cat_list)

"""Functions for the items"""


@app.route('/item/<sku>/<seller_id>/<buyer_id>/review', methods=["POST"])
def review(sku, seller_id, buyer_id):
    query = db.session.query(relations.Item.title).filter(relations.Item.sku == sku).first()
    item = {'title': query.title}
    form = WriteReviewForm()
    new_review = relations.Review(seller_id=seller_id, buyer_id=buyer_id, sku=sku, item_rating=form.star_rating,
                                  written_review=form.written_rating)
    db.session.add(new_review)
    db.session.commit()
    # TODO: Validate that item being reviewed is sold by seller and has been bought by buyer
    return render_template('review.html', item=item, form=form)


@app.route('/item/<sku>', methods=["GET"])
def item_page(sku):
    query = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price,
                             relations.Item.rating, relations.Item.description, relations.Item.seller,
                             relations.Item.image, relations.Item.quantity).filter(relations.Item.sku == sku)
    query = query[0]
    item = {'sku': query.sku, 'title': query.title, 'category': query.category, 'price': query.price,
            'rating': query.rating, 'description': query.description, 'seller': query.seller,
            'image': query.image, 'quantity': query.quantity}
    cat_list = list()
    categories = db.session.query(relations.Item.category).distinct()
    for row in categories:
        temp = {'name': row.category}
        cat_list.append(temp)
    return render_template('item.html', items=item, categories=cat_list)


@app.route("/addItem", methods=['GET', 'POST'])
def add_item():
    form = AddItemForm()
    if request.method == 'POST':
        print("Add Item Form Validated")
        new_item = relations.Item(sku=form.sku.data, title=form.title.data, description=form.description.data,
                                  price=form.price.data, category=form.category.data, quantity=form.quantity.data,
                                  rating=0, seller=form.seller.data, image=form.image.data)
        db.session.add(new_item)
        db.session.commit()
        flash('Item added to inventory.')
        return redirect(url_for('main'))
    return render_template('additem.html', form=form)


@app.route("/removeItem", methods=["GET", "POST"])
def remove_item():
    sku = request.get_json()
    item = db.session.query(relations.Item).filterby(sku=sku["sku"])
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('main'))


@app.route("/<sku>/modifyItem", methods=["GET", "POST"])
def modify_item(sku):
    # TODO: validate that item sku is being sold by seller
    query = db.session.query(relations.Item.title,
                             relations.Item.description, relations.Item.category, relations.Item.quantity,
                             relations.Item.price, relations.Item.image).filter(relations.Item.sku == sku).first()
    item = {'title': query.title,
            'description': query.description, 'category': query.category, 'quantity': query.quantity,
            'price': query.price, 'image': query.image}
    if request.method == 'GET':
        form = EditItemForm(formdata=MultiDict(
            {'title': query.title, 'description': query.description, 'category': query.category,
             'quantity': query.quantity,
             'price': query.price, 'image': query.image}))
        form.category.choices = [x.name for x in db.session.query(relations.Category.name).all()]
    elif request.method == 'POST':
        form = EditItemForm()
        relations.Item.updateItem(form.title.data, form.description.data, form.category.data, form.quantity.data,
                                  form.price.data, form.image.data, sku)
        print("Edit Item Form Validated")
        db.session.commit()
    return render_template('edit_item.html', item=item, form=form)


"""Functions for search results"""


@app.route('/<search>/results', methods=['GET', 'POST'])
def search_results(search):
    result = list()
    query = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price,
                             relations.Item.rating, relations.Item.description).filter(relations.Item.title == search)
    for row in query:
        temp = {'sku': row.sku, 'title': row.title, 'category': row.category, 'price': row.price,
                'rating': row.rating, 'description': row.description}
        result.append(temp)
    return jsonify(result)


"""Functions for the cart"""


@app.route('/cart')
@login_required
def cart_page():
    buyer_id = current_user.id
    result = list()
    total_cost = 0
    query = db.session.query(relations.Cart.buyer_id, relations.Cart.sku).filter(relations.Cart.buyer_id == buyer_id)
    for row in query:
        item_query = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category,
                                      relations.Item.price,
                                      relations.Item.rating, relations.Item.description, relations.Item.seller,
                                      relations.Item.image).filter(relations.Item.sku == row.sku)
        item_query = item_query[0]
        item = {'sku': item_query.sku, 'title': item_query.title, 'category': item_query.category,
                'price': item_query.price, 'rating': item_query.rating, 'description': item_query.description,
                'seller': item_query.seller, 'image': item_query.image}
        total_cost = total_cost + item_query.price
        result.append(item)
        cat_list = list()
        categories = db.session.query(relations.Item.category).distinct()
        for r in categories:
            temp = {'name': r.category}
            cat_list.append(temp)
    return render_template('cart.html', items=result, user=buyer_id, cost=round(total_cost, 2), categories=cat_list)


@app.route("/addToCart", methods=["GET", "POST"])
@login_required
def add_to_cart():
    if request.method == 'POST':
        sku = request.form['sku']
        buyer_id = current_user.id  # request.form['buyer_id']
        new_item = relations.Cart(sku=sku, buyer_id=buyer_id)
        db.session.add(new_item)
        db.session.commit()
        flash('Item added to cart.')
    return redirect(url_for('main'))


@app.route("/removeFromCart/<sku>", methods=["GET", "POST"])
@login_required
def remove_from_cart(sku):                                           # THIS DOES NOT YET WORK !!!!!!!
    buyer_id = current_user.id
    print(sku)
    # relations.Cart.delete_from_cart(sku, buyer_id)
    item = db.session.query(relations.Cart).filter(relations.Cart.sku == sku, relations.Cart.buyer_id == buyer_id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect('/cart')   # Change the 1 to be a buyer_id variable


""" Functions for checkout """


@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    user_id = current_user.id
    # Address query
    address = get_address()
    # Cart query
    cart_result, total_cost = get_cart_info()
    credit_card_query = db.session.query(relations.PaysWith).filter(relations.PaysWith.buyer_id == user_id).first()
    if credit_card_query is None:
        card = 'No card on file.'
    else:
        card = credit_card_query.credit_card
    card_dict = {'card': card}
    return render_template('checkout.html', address=address,
                           cart=cart_result, totalcost=round(total_cost, 2), card=card_dict)


def get_address():
    user_id = current_user.id
    address_query = db.session.query(relations.User.address).filter(relations.User.id == user_id).first()
    address = {'address': address_query.address}
    return address


def get_cart_info():
    user_id = current_user.id
    cart_result = list()
    total_cost = 0
    cart_query = db.session.query(relations.Cart.buyer_id,
                                  relations.Cart.sku).filter(relations.Cart.buyer_id == user_id)
    for row in cart_query:
        item_query = db.session.query(relations.Item.sku, relations.Item.title,
                                      relations.Item.category, relations.Item.price,
                                      relations.Item.rating, relations.Item.description,
                                      relations.Item.seller, relations.Item.image,
                                      relations.Item.quantity).filter(relations.Item.sku == row.sku)
        item_query = item_query[0]
        item = {'sku': item_query.sku, 'title': item_query.title, 'category': item_query.category,
                'price': item_query.price, 'rating': item_query.rating, 'description': item_query.description,
                'seller': item_query.seller, 'image': item_query.image, 'quantity': item_query.quantity}
        total_cost = total_cost + item_query.price
        cart_result.append(item)
    return cart_result, total_cost


@app.route('/placeorder', methods=["GET", "POST"])
@login_required
def place_order():
    buyer_id = current_user.id
    cart_result, total_cost = get_cart_info()
    address = get_address()
    credit_card_query = db.session.query(relations.PaysWith).filter(relations.PaysWith.buyer_id == buyer_id).first()
    if credit_card_query is None:
        card_dict = {'card': 'No card on file.'}
        flash('ERROR: No credit card on file')
        return render_template('checkout.html', address=address, cart=cart_result,
                               totalcost=round(total_cost, 2), card=card_dict)
    for item in cart_result:
        if item['quantity'] > 0:
            # remove items from cart
            cart_query = db.session.query(relations.Cart).filter(relations.Cart.sku == item["sku"],
                                                                 relations.Cart.buyer_id == buyer_id).first()
            db.session.delete(cart_query)
            db.session.commit()
            item_query = db.session.query(relations.Item).filter(relations.Item.sku == item["sku"]).first()
            item_query.quantity = item["quantity"] - 1
            relations.Item.updateItem(item_query.title, item_query.description, item_query.category,
                                      item_query.quantity, item_query.price, item_query.image, item_query.sku)
            db.session.commit()
            flash('Purchase Successful.')
        else:
            total_cost = total_cost - item["price"]
            flash(f'ERROR: Could not purchase item {item["title"]}')
            cart_result.remove(item)
    # Add order to order table

    new_order = relations.Order(total_price=total_cost, buyer_id=buyer_id)
    db.session.add(new_order)
    db.session.commit()
    print(new_order.order_id)
    for item in cart_result:
        new_oc = relations.OrdersContain(order_id=new_order.order_id, sku=item["sku"],
                                         quantity_ordered=item["quantity"], price_at_order=item["price"])
        db.session.add(new_oc)
        db.session.commit()
    # Add to places
    new_places = relations.Places(order_id=new_order.order_id, buyer_id=buyer_id)
    db.session.add(new_places)
    db.session.commit()
    new_payment = relations.RequiresPayment(order_id=new_order.order_id,
                                            credit_card_number=credit_card_query.credit_card)
    db.session.add(new_payment)
    db.session.commit()
    return redirect(url_for('main'))


"""Functions for the user profile"""


@app.route('/profile', methods=["GET"])
@login_required
def profile_page():
    query = db.session.query(relations.User.id, relations.User.is_seller, relations.User.password,
                             relations.User.email, relations.User.question, relations.User.answer,
                             relations.User.address).filter(relations.User.id == current_user.id).first()
    user = {'id': query.id, 'is_seller': query.is_seller, 'password': query.password,
            'email': query.email, 'question': query.question, 'answer': query.answer,
            'address': query.address}
    if current_user.is_seller == 0:
        return render_template('user_profile.html', user=user)
    if current_user.is_seller == 1:
        # TODO: validate that user_id is a seller
        print('seller confirmed')
        return render_template('seller_profile.html', user=user)


@app.route("/<user_id>/profile/edit", methods=["POST", "GET"])
def edit_profile(user_id):
    query = db.session.query(relations.User.password,
                             relations.User.email, relations.User.question, relations.User.answer,
                             relations.User.address).filter(relations.User.id == user_id).first()
    user = {'password': query.password,
            'email': query.email, 'question': query.question, 'answer': query.answer,
            'address': query.address}
    if request.method == 'GET':
        form = EditProfileForm(formdata=MultiDict(
            {'email': query.email, 'password': query.password, 'address': query.address, 'question': query.question,
             'answer': query.answer}))
    elif request.method == 'POST':
        form = EditProfileForm()
        relations.User.updateUser(form.password.data, form.email.data, form.question.data, form.answer.data,
                                  form.address.data, user_id)
        print("Edit Profile Form Validated")
        db.session.commit()
    return render_template('edit_profile.html', user=user, form=form)


@app.route("/<user_id>/sellerpage", methods=["POST", "GET"])
def seller_page(user_id):
    result = list()
    query = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price,
                             relations.Item.rating, relations.Item.seller, relations.Item.image).filter(
        relations.Item.seller == user_id)
    for row in query:
        temp = {'sku': row.sku, 'title': row.title, 'category': row.category, 'price': row.price,
                'rating': row.rating, 'seller': row.seller, 'image': row.image}
        result.append(temp)

    return render_template('seller_page.html', items=result, user=1)


@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def change_password():
    in_dict = request.get_json()
    user = User.query.filter_by(id=in_dict["id"]).first()
    user.password = in_dict["password"]
    db.session.commit()
    return "Password successfully updated."


@app.route("/profile/history", methods=["GET", "POST"])
def order_history():
    order_result = list()
    user_id = current_user.id
    history_query = db.session.query(relations.Order.order_id, relations.Order.time_stamp,
                                     relations.Order.total_price).filter(relations.Order.buyer_id == user_id)
    for row in history_query:
        order = {'order_id': row.order_id, 'time_stamp': row.time_stamp,
                 'total_price': row.total_price}
        order_result.append(order)
    return render_template('orderhistory.html', orders=order_result)


@app.route("/profile/history/<order_id>", methods=["GET", "POST"])
def order_info(order_id):
    order_query = db.session.query(relations.OrdersContain.sku,
                                   relations.OrdersContain.price_at_order,
                                   relations.OrdersContain.quantity_ordered).filter(
        relations.OrdersContain.order_id == order_id)
    info_query = db.session.query(relations.Order.time_stamp,
                                  relations.Order.total_price).filter(relations.Order.order_id == order_id)
    info_query = info_query[0]
    info_dict = {'order_id': order_id, 'time_stamp': info_query.time_stamp, 'total_price': info_query.total_price}
    item_list = list()
    for row in order_query:
        item_query = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category,
                                      relations.Item.price,
                                      relations.Item.rating, relations.Item.description, relations.Item.seller,
                                      relations.Item.image,
                                      relations.Item.quantity).filter(relations.Item.sku == row.sku)
        query = item_query[0]
        item = {'sku': query.sku, 'title': query.title, 'category': query.category, 'price': row.price_at_order,
                'rating': query.rating, 'description': query.description, 'seller': query.seller,
                'image': query.image, 'quantity': row.quantity_ordered}
        item_list.append(item)
    return render_template('orderinfo.html', orders=item_list, info=info_dict)


if __name__ == '__main__':
    app.run()
    # print(db.session.query(relations.User.id, relations.User.is_buyer).all())
