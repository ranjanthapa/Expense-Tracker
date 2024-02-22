from flask import Flask
from config import DatabaseConfig, initialize_sql

app = Flask(__name__)
app.config.from_object(DatabaseConfig)

mysql = initialize_sql(app)


if __name__ == '__main__':
    app.run(debug=True)
