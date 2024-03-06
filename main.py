from flask import Flask, render_template
from config import DatabaseConfig, initialize_sql

app = Flask(__name__)
app.config.from_object(DatabaseConfig)

mysql = initialize_sql(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/income')
def income():
    return render_template('income.html')


@app.route('/transaction')
def transaction():
    return render_template("transaction.html")


@app.route('/edit-profile')
def edit_profile():
    return render_template("edit_profile.html")


@app.route('/register')
def register():
    return render_template("registration.html")


@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
