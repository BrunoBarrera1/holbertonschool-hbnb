from flask import Flask
from app.api import api

def create_app():
    app = Flask(__name__)
    api.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
