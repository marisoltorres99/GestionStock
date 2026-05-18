from flask import Blueprint, render_template
from models.venta import Venta
from datetime import datetime, timedelta
from sqlalchemy import func
from models.db import db

informe_bp = Blueprint("informe", __name__)

@informe_bp.route("/informes")
def listar():
    return render_template("informes/index.html")

@informe_bp.route("/informes/ventasDelDia")
def ventasDelDia():

    inicio_hoy = datetime.today().replace(
    hour=0,
    minute=0,
    second=0,
    microsecond=0
    )

    inicio_manana = inicio_hoy + timedelta(days=1)
    
    ventasDiarias = Venta.query.filter(Venta.fecha >= inicio_hoy, Venta.fecha < inicio_manana).all()

    totalRecaudadoHoy = (
        db.session.query(func.sum(Venta.total))
        .filter(
            Venta.fecha >= inicio_hoy,
            Venta.fecha < inicio_manana
        )
        .scalar()
    ) or 0

    return render_template("informes/ventasDiarias.html", totalRecaudadoHoy=totalRecaudadoHoy, ventas=ventasDiarias)