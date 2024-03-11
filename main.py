from flask import Flask, render_template, request, redirect, url_for

from config import DatabaseConfig, initialize_sql
from expense_tracker.user.user_manager import UserManager
from expense_tracker.user.exception import UserExists
from flask import flash
from flask_login import LoginManager, logout_user, current_user
from expense_tracker.user.user_manager import User

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
    user_data = user_manager.get_user_by_id(user_id)
    if user_data:
        user = User(user_data)
        return user
    else:
        return None


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/income')
def income():
    return render_template('income.html')


@app.route('/transaction')
def transaction():
    return render_template("transaction.html")


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
            print(user_manager.get_user_by_id(email))
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
