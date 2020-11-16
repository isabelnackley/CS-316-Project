# database
from flask import Flask, render_template, redirect, url_for, jsonify, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import os
from sqlalchemy import or_, func, and_
import pymysql
from werkzeug.datastructures import MultiDict

import relations
from forms import AddItemForm, EditProfileForm, EditItemForm, WriteReviewForm, LoginForm, ForgotPasswordForm, \
    VerifyEmailForm, CreateProfileForm, SearchItemsForm, AddPaymentMethodForm

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:password@152.3.52.135/test1'

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

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
    flash("You must be logged in to view that page.")
    return redirect(url_for('login'))



@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in")
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(relations.User).filter_by(email=form.email.data).first()
        if user and user.password==form.password.data:
            login_user(user)
            return redirect(url_for('main'))
        flash("Invalid Username and/or Password")
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout', methods=["GET"])
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("You have logged out")
        return redirect(url_for('main'))
    flash("You are not logged in")
    return redirect(url_for('main'))

@app.route('/verifyemail', methods=["GET", "POST"])
def verify_email():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = VerifyEmailForm()
    if form.validate_on_submit():
        user = db.session.query(relations.User).filter_by(email=form.email.data).first()
        if user:
            return redirect(url_for('forgot_password', user=user.id))
        flash("Account does not exist")
        return redirect(url_for('verify_email'))
    return render_template('verify_email.html', form=form)


@app.route('/<user>/forgotpassword', methods=["POST", "GET"])
def forgot_password(user):
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    user_object = db.session.query(relations.User).filter_by(id=user).first()
    question = user_object.question
    password= ""
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        if user and user_object.answer==form.answer.data:
            password= user_object.password
            return render_template('forgot_password.html', form=form, password=password, question=question)
        flash("Invalid Answer")
        return redirect(url_for('forgot_password', user=user))
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

  
@app.route("/create_profile", methods=['GET', 'POST'])
def create_profile():
    form = CreateProfileForm()
    if form.validate_on_submit():
        existing_user = db.session.query(relations.User).filter_by(email=form.email.data).first()
        if existing_user is None:
            user_id = len(db.session.query(relations.User).all()) + 1
            if form.is_seller.data == 'Yes':
                seller = 1
                new_seller = relations.Seller(id=user_id, rating=None)
                db.session.add(new_seller)
            elif form.is_seller.data == 'No':
                seller = 0
            new_user = relations.User(id=user_id, is_seller=seller, email=form.email.data,
                                      password=form.password.data, question=form.question.data,
                                      answer=form.answer.data, address=form.address.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('You are now logged in')
            return redirect(url_for('main'))
        flash('Account already exists for this user')
        return redirect(url_for('create_profile'))
    return render_template('create_profile.html', form=form)


"""Functions for the items"""


@app.route('/item/<sku>/review', methods=["GET", "POST"])
@login_required
def review(sku):
    item = db.session.query(relations.Item).filter_by(sku = sku).first()
    title = {'title': item.title}
    form = WriteReviewForm()
    if form.validate_on_submit():
        existing_review = db.session.query(relations.Review).filter(and_(relations.Review.sku==sku, relations.Review.buyer_id==current_user.id)).first()
        if existing_review == None:
            new_review = relations.Review(seller_id=item.seller, buyer_id=current_user.id, sku=sku, item_rating=form.star_rating.data, seller_rating=0,
                                          written_review=form.written_rating.data)

            db.session.add(new_review)
            item_rating = db.session.query(func.avg(relations.Review.item_rating).label('average')).filter_by(sku=sku).scalar()
            seller_rating = db.session.query(func.avg(relations.Review.item_rating)).filter_by(seller_id=item.seller).scalar()
            db.session.query(relations.Item).filter_by(sku=sku).update({relations.Item.rating: item_rating})
            print(item.seller)
            print(seller_rating)
            db.session.query(relations.Seller).filter_by(id=item.seller).update({relations.Seller.rating: seller_rating})
            db.session.commit()
            return redirect(url_for('item_page', sku=sku))
        flash("You have already reviewed this item")
        return redirect(url_for('item_page', sku=sku))
    return render_template('review.html', item=title, form=form)


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
    reviews = db.session.query(relations.Review.item_rating, relations.Review.written_review).filter_by(sku=sku)
    for row in categories:
        temp = {'name': row.category}
        cat_list.append(temp)
    return render_template('item.html', items=item, categories=cat_list, reviews=reviews)


@app.route("/addItem", methods=['GET', 'POST'])
@login_required
def add_item():
    form = AddItemForm()
    sku = len(db.session.query(relations.Item).all()) + 1
    if form.validate_on_submit():
        print(form.quantity.data)
        new_item = relations.Item(sku=sku, title=form.title.data, description=form.description.data,
                                  price=form.price.data, category=form.category.data, quantity=form.quantity.data,
                                  rating=0, seller=current_user.id, image=form.image.data)
        db.session.add(new_item)

        db.session.commit()
        x = db.session.query(relations.Item.quantity).filter_by(sku=sku).first()
        print(x)
        flash('Item added to inventory.')
        return redirect(url_for('main'))
    return render_template('additem.html', form=form)


'''@app.route("/removeItem", methods=["GET", "POST"])
def remove_item():
    sku = request.get_json()
    item = db.session.query(relations.Item).filterby(sku=sku["sku"])
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('main'))'''


@app.route("/<sku>/modifyItem", methods=["GET", "POST"])
@login_required
def modify_item(sku):
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
        form.category.choices = [x.category for x in db.session.query(relations.Item.category).distinct()]
    elif request.method == 'POST':
        print('yes')
        form = EditItemForm()
        #if form.validate_on_submit():
        modify_item_query = db.session.query(relations.Item).filter_by(sku=sku).first()
        relations.Item.updateItem(form.title.data,
                                   form.description.data,
                                   form.category.data,
                                   form.quantity.data,
                                   form.price.data,
                                   form.image.data, sku)
        db.session.commit()
        return redirect(url_for('seller_page'))
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
        return render_template('seller_profile.html', user=user)

@app.route("/paymentmethod", methods=["POST", "GET"])
@login_required
def payment_method():
    payment_info = db.session.query(relations.PaysWith).filter(relations.PaysWith.buyer_id==current_user.id).all()
    form = AddPaymentMethodForm()
    if form.validate_on_submit():
        existing_card = db.session.query(relations.PaysWith).filter(relations.PaysWith.credit_card==form.credit_card.data).first()
        if existing_card == None:
            #new_payment = relations.Payment(credit_card=form.credit_card.data, address=form.address.data)
            link_to_buyer = relations.PaysWith(credit_card=form.credit_card.data, buyer_id=current_user.id)
            #db.session.add(new_payment)
            db.session.add(link_to_buyer)
            db.session.commit()
            flash("New Payment Method Added")
            return redirect(url_for('payment_method'))
        flash('This card is already being used on this website')
        return redirect(url_for('payment_method'))
    return render_template('payment_methods.html', payment_info=payment_info, form=form)

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
        if form.validate_on_submit() :
            existing_user = db.session.query(relations.User).filter_by(email=form.email.data).first()
            if existing_user == None or existing_user.email == current_user.email:
                relations.User.updateUser(form.password.data, form.email.data, form.question.data, form.answer.data,
                                      form.address.data, user_id)
                db.session.commit()
                return redirect(url_for('profile_page'))
            flash("Account already exists with this email")
    return render_template('edit_profile.html', user=user, form=form)


@app.route("/sellerpage", methods=["GET"])

def seller_page():
    result = list()
    query = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price,
                             relations.Item.rating, relations.Item.seller, relations.Item.image).filter(
        relations.Item.seller == current_user.id)
    for row in query:
        temp = {'sku': row.sku, 'title': row.title, 'category': row.category, 'price': row.price,
                'rating': row.rating, 'seller': row.seller, 'image': row.image}
        result.append(temp)

    seller_rating = db.session.query(relations.Seller.rating).filter(relations.Seller.id == current_user.id).scalar()

    return render_template('seller_page.html', items=result, rating=seller_rating)


'''@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def change_password():
    in_dict = request.get_json()
    user = User.query.filter_by(id=in_dict["id"]).first()
    user.password = in_dict["password"]
    db.session.commit()
    return "Password successfully updated."'''


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
