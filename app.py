from dotenv import load_dotenv
from flask import Flask
from .routes import queries_bp
from .routes import accident_bp


load_dotenv()

app = Flask(__name__)

app.config.from_object('app.config.Config')





app.register_blueprint(accident_bp)
app.register_blueprint(queries_bp)


if __name__ == '__main__':
    app.run()
