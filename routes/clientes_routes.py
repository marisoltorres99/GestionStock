from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import func
from models.cliente import Cliente
from models.venta import Venta
from models.pago import Pago
from models.db import db

cliente_bp = Blueprint("cliente", __name__)

@cliente_bp.route("/clientes")
def listar():
    clientes = Cliente.query.all()
    return render_template("clientes/index.html", clientes=clientes)


@cliente_bp.route("/clientes/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]

        nuevo = Cliente(nombre=nombre, telefono=telefono)

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("cliente.listar"))

    return render_template("clientes/form.html")


@cliente_bp.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    cliente = db.session.get(Cliente, id)

    if not cliente:
        return "Cliente no encontrado"

    if request.method == "POST":
        cliente.nombre = request.form["nombre"]
        cliente.telefono = request.form["telefono"]

        db.session.commit()

        return redirect(url_for("cliente.listar"))

    return render_template("clientes/form.html", cliente=cliente)


@cliente_bp.route("/clientes/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    cliente = db.session.get(Cliente, id)

    if cliente.ventas or cliente.pagos:
        flash(
            "No se puede eliminar un cliente con ventas o pagos registrados",
            "danger"
        )

        return redirect(url_for("cliente.listar"))

    if cliente:
        db.session.delete(cliente)
        db.session.commit()
    
    flash("Cliente eliminado correctamente", "success")

    return redirect(url_for("cliente.listar"))

@cliente_bp.route("/clientes/<int:id>", methods=["GET"])
def calcularDeuda(id):
    
    cliente = db.session.get(Cliente, id)
    
    monto_ventas_fiadas = (
        db.session.query(func.sum(Venta.total))
        .filter(
            Venta.cliente_id == id, 
            Venta.tipo_pago == "fiado"
            )
        .scalar() or 0
    )

    monto_pagos = (db.session.query(func.sum(Pago.monto))
                   .filter(
                       Pago.cliente_id == id
                   )
                   .scalar() or 0
    )

    deuda = monto_ventas_fiadas - monto_pagos

    ventas = cliente.ventas
    pagos = cliente.pagos

    return render_template("clientes/detalle.html", cliente=cliente, deuda=deuda, 
                           monto_pagos=monto_pagos, monto_ventas_fiadas=monto_ventas_fiadas, ventas=ventas, pagos=pagos)

