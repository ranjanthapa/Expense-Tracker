from datetime import datetime, date

from flask import Flask, render_template, request, redirect, url_for
from config import DatabaseConfig, initialize_sql
from expense_tracker.user.user_manager import UserManager
from expense_tracker.user.exception import UserExists
from expense_tracker.transcation.income import add_income, get_income_by_user_id, get_total_incomes
from expense_tracker.transcation.expense import add_expense, get_all_expenses, get_total_expense
from flask import flash
from flask_login import LoginManager, logout_user, current_user
from expense_tracker.user.user_manager import User

import pprint

app = Flask(__name__)
app.config.from_object(DatabaseConfig)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'ABFSK'
mysql = initialize_sql(app)


@login_manager.user_loader
def load_user(user_id: int):
    print(type(user_id))
    user_manager = UserManager(mysql)
    user_data = user_manager.get_user_info(user_id)
    if user_data:
        user = User(user_data)
        return user
    else:
        return None


@app.route('/')
def home():
    user = current_user.get_id()
    recent_transactions: list = []
    income_list = get_income_by_user_id(user, mysql)
    for income in income_list[:7]:
        income['transaction_type'] = 'income'
        recent_transactions.append(income)

    expense_list = get_all_expenses(user, mysql)
    for expense in expense_list[:7]:
        expense['transaction_type'] = 'expense'
        recent_transactions.append(expense)

    pprint.pprint(recent_transactions)
    return render_template('home.html', recent_transactions=recent_transactions)


@app.route('/income', methods=['GET', 'POST'])
def income():
    user_id = current_user.get_id()
    income_list = get_income_by_user_id(user_id, mysql)
    # pprint.pprint(income_list)
    total_income = get_total_incomes(user_id, mysql)
    if request.method == "POST":
        data = request.form
        is_added = add_income(user_id, amount=int(data.get('amount')), source=data.get('source'),
                              remark=data.get('remark'),
                              receive_date=datetime.strptime(data.get('receive_date'), "%Y-%m-%d"),
                              mysql=mysql)
        if is_added:
            return redirect(url_for('income'))
    return render_template('income.html', income_list=income_list, total_income=total_income)


@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    user_id = current_user.get_id()
    expense_list = get_all_expenses(user_id, mysql)
    total_expense = get_total_expense(user_id, mysql)
    print(expense_list)
    if request.method == 'POST':
        data = request.form
        print(data.to_dict())
        is_added = add_expense(user_id, amount=int(data.get('amount')),
                               paid_date=datetime.strptime(data.get('paid_date'), "%Y-%m-%d"),
                               paid_to=data.get('paid_to'), remark=data.get('remark'), mysql=mysql)
        if is_added:
            flash('Expense added', 'success')
            return redirect(url_for('transaction'))
    return render_template("transaction.html", expense_list=expense_list, total_expense=total_expense)


@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == "POST":
        user_manager = UserManager(mysql)
        data = request.form.to_dict()

        user_id = current_user.get_id()
        is_profile_update = user_manager.update_profile(user_id, data)
        if is_profile_update:
            flash("Profile Updated successfully", "success")
            return redirect(url_for('edit_profile'))
    return render_template("edit_profile.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        data = request.form.to_dict()
        print(data)
        email = data.get('email')
        phone_number = data.get('phone')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        full_name = data.get('full_name')

        if password == confirm_password:
            user_manager = UserManager(mysql)
            print(user_manager.get_user_info(email))
            try:
                user_manager.register_user(email, password, phone_number, full_name)
                flash('User created successfully', 'success')
            except UserExists:
                flash("User exists with the same email", "error")
            return redirect('/register')
        else:
            flash('Passwords do not match', 'error')
    return render_template("registration.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user_manager = UserManager(mysql)
        is_user_login = user_manager.login(email, password)
        if is_user_login:
            return redirect('/')
        else:
            flash("False Credential", "error")
            return redirect('/login')
    return render_template("login.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
