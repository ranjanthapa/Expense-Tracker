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


if __name__ == '__main__':
    app.run(debug=True)
