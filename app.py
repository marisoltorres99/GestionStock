from flask import Flask, render_template
from models.db import db
from routes.productos_routes import producto_bp
from routes.clientes_routes import cliente_bp
from routes.ventas_routes import venta_bp
from routes.pago_routes import pago_bp
from routes.informes_routes import informe_bp
from flask_migrate import Migrate
import os

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")

if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tienda.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

#flask migrate
migrate = Migrate(app, db)

# registrar blueprint
app.register_blueprint(producto_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(venta_bp)
app.register_blueprint(pago_bp)
app.register_blueprint(informe_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)