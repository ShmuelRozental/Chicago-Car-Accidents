from dotenv import load_dotenv
from flask import Flask
from dal.connect import database

load_dotenv()

app = Flask(__name__)

app.config.from_object('config.Config')


from routes.insert_routes import accident_bp
app.register_blueprint(accident_bp)


if __name__ == '__main__':
    app.run()
