from flask import Flask
from models.db import db
from routes.productos_routes import producto_bp
from routes.clientes_routes import cliente_bp
from routes.ventas_routes import venta_bp
from routes.pago_routes import pago_bp
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tienda.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

#flask migrate
migrate = Migrate(app, db)

# registrar blueprint
app.register_blueprint(producto_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(venta_bp)
app.register_blueprint(pago_bp)

@app.route("/")
def home():
    return "Proyecto Flask funcionando 🚀"

if __name__ == "__main__":
    app.run(debug=True)