from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.pago import Pago
from models.cliente import Cliente
from models.db import db

pago_bp = Blueprint("pago", __name__)

@pago_bp.route("/pagos")
def listar():
    pagos = Pago.query.order_by(Pago.fecha.desc()).all()
    return render_template("pagos/index.html", pagos=pagos)

@pago_bp.route("/pagos/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        cliente_id = int(request.form.get("cliente_id"))
        monto = float(request.form.get("monto"))

        pago = Pago(monto=monto, cliente_id=cliente_id)

        db.session.add(pago)
        db.session.commit()

        flash("Pago registrado correctamente", "success")

        return redirect(url_for("pago.listar"))
    else:
        clientes = Cliente.query.all()
        return render_template("pagos/form.html", clientes=clientes)