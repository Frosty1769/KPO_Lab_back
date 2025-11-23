from flask import Flask
from flask_cors import CORS

from endpoints import user, products

from db import db
from scr.core import settings

app = Flask(__name__)
app.config.from_object(settings)

CORS(app, 
     supports_credentials=True, 
     origins=["http://localhost:5173", "http://127.0.0.1:5173"],
     allow_headers=["Content-Type"],
     expose_headers=["Set-Cookie"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
db.init_app(app)

# Регистрация blueprints
app.register_blueprint(user.bp, url_prefix="/api/user")
app.register_blueprint(products.bp, url_prefix="/api/products")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("База данных инициализирована")
    
    app.run(host='0.0.0.0', port=5000, debug=True)