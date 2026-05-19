from flask import Blueprint, render_template
from models.venta import Venta
from models.detalle_venta import DetalleVenta
from models.producto import Producto
from models.cliente import Cliente
from datetime import datetime, timedelta
from sqlalchemy import func, select
from models.db import db
from services.deuda_service import calcular_deuda_cliente

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

@informe_bp.route("/informes/productosMasVendidos")
def productosMasVendidos():
    
    stmt = (
        select(Producto.nombre, func.sum(DetalleVenta.cantidad).label("cantidadProductoVendido"))
        .join(DetalleVenta, Producto.id == DetalleVenta.producto_id)
        .group_by(Producto.id, Producto.nombre)
        .order_by(func.sum(DetalleVenta.cantidad).desc())
    )

    detallesVentas = db.session.execute(stmt).all()

    return render_template("informes/productosMasVendidos.html", detallesVentas=detallesVentas)

@informe_bp.route("/informes/clientesConDeudas")
def clientesConDeudas():
    
    clientes = db.session.query(Cliente).all()

    clientes_con_deudas = []

    for cliente in clientes:
        monto_ventas_fiadas, monto_pagos, deuda = calcular_deuda_cliente(cliente.id)
        if deuda > 0:
            clientes_con_deudas.append({
                "cliente": cliente,
                "deuda": deuda,
                "pagos": monto_pagos,
                "ventas": monto_ventas_fiadas
            })
    
    clientes_con_deudas.sort(
        key=lambda x: x["deuda"],
        reverse=True
    )

    return render_template("informes/clientesConDeudas.html", clientes_con_deudas=clientes_con_deudas)