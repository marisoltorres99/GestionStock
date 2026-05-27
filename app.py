from flask import Flask, render_template
from models.db import db
from routes.productos_routes import producto_bp
from routes.clientes_routes import cliente_bp
from routes.ventas_routes import venta_bp
from routes.pago_routes import pago_bp
from routes.informes_routes import informe_bp
from flask_migrate import Migrate
from models.cliente import Cliente
from models.producto import Producto
from models.venta import Venta
from sqlalchemy import func
from datetime import datetime, timedelta
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

#flash
app.secret_key = "clave_secreta"

@app.route("/")
def home():

    total_clientes = Cliente.query.count()

    total_productos = Producto.query.count()

    total_ventas = Venta.query.count()

    inicio_hoy = datetime.today().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    inicio_manana = inicio_hoy + timedelta(days=1)

    ventas_hoy = (
        Venta.query.filter(
            Venta.fecha >= inicio_hoy,
            Venta.fecha < inicio_manana
        ).count()
    )

    inicio_mes = datetime.today().replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    recaudacion_mes = (
        db.session.query(func.sum(Venta.total))
        .filter(Venta.fecha >= inicio_mes)
        .scalar() or 0
    )

    return render_template(
        "index.html",
        total_clientes=total_clientes,
        total_productos=total_productos,
        total_ventas=total_ventas,
        ventas_hoy=ventas_hoy,
        recaudacion_mes=recaudacion_mes
    )

if __name__ == "__main__":
    app.run(debug=True)