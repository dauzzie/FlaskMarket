from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from market import app
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm, AddItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user
from market.item_service import check_exist, add_item

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        # Purchase item
        purchased_item = request.form.get('purchased_item')
        p_item = Item.query.filter_by(name=purchased_item).first()
        if p_item:
            if current_user.can_purchase(p_item):
                p_item.purchase(current_user)
                flash(f'Congratulations! You purchased {p_item.name} for {p_item.price}!', category='success')
            else:
                flash(f'Unfortunately, you don\'t have enough money to purchase {p_item.name}', category='danger')
        # Sell item
        sold_item = request.form.get('sold_item')
        s_item = Item.query.filter_by(name=sold_item).first()
        if s_item:
            if current_user.can_sell(s_item):
                s_item.sell(current_user)
                flash(f'Congratulations! You sold {s_item.name} for ${s_item.price}!', category='success')
            else:
                flash(f'Something went wrong with selling {s_item.name}', category='danger')

        return redirect(url_for('market_page'))
    
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, selling_form=selling_form, owned_items = owned_items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                                email_address=form.email.data,
                                password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as {user_to_create.username}', 
            category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error in creating new user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not matched! Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for("home_page"))

@app.route('/add_item', methods=["GET", "POST"])
def add_item_page():
    form = AddItemForm()
    if form.validate_on_submit():
        print(form, form.name, form.name.data)
        if not check_exist(form.name.data):
            add_item(form)
            flash(f'Success! You added {form.name.data} to the market!', category='success')
            return redirect(url_for('market_page'))
        else:
            flash(f'Unfortunately the item already existed in the market', category='danger')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error in creating new item: {err_msg}', category='danger')
    
    return render_template('add_item.html', form=form)


            

