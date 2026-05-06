from flask import Blueprint, render_template, request, redirect, url_for
from models.venta import Venta
from models.cliente import Cliente
from models.producto import Producto
from models.detalle_venta import DetalleVenta
from models.db import db
from datetime import datetime

venta_bp = Blueprint("venta", __name__)

@venta_bp.route("/ventas")
def listar():
    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template("ventas/index.html", ventas=ventas)

@venta_bp.route("/ventas/<int:id>")
def detalle(id):
    venta = db.session.get(Venta, id)

    if not venta:
        return "Venta no encontrada"

    detalles = venta.detalles

    return render_template("ventas/detalle.html", venta=venta, detalles=detalles)

@venta_bp.route("/ventas/crear", methods=["GET", "POST"])
def crear():

    if request.method == "POST":

        cliente_id = request.form.get("cliente_id") or None
        productos_ids = request.form.getlist("producto_id")
        cantidades = request.form.getlist("cantidad")
        tipo_pago = request.form["tipo_pago"]

        if tipo_pago == "fiado" and not cliente_id:
            return "Las ventas fiadas requieren un cliente"

        venta = Venta(cliente_id=cliente_id, tipo_pago=tipo_pago, total=0)
        db.session.add(venta)
        db.session.flush()

        total = 0

        for i in range(len(productos_ids)):
            producto = db.session.get(Producto, int(productos_ids[i]))

            if not producto:
                return "Producto no encontrado"
            
            cantidad = int(cantidades[i])

            if cantidad == 0:
                continue

            if producto.stock < cantidad:
                db.session.rollback()
                return "Stock insuficiente"
            
            subtotal = producto.precio * cantidad

            detalle = DetalleVenta(
                venta_id=venta.id,
                producto_id=producto.id, 
                cantidad=cantidad,
                precio_unitario=producto.precio)
            
            db.session.add(detalle)

            producto.stock = producto.stock - cantidad

            total += subtotal

        if total == 0:
            return "No seleccionaste productos"
        venta.total = total
        db.session.commit()

        return redirect(url_for("venta.listar"))

    # GET
    clientes = Cliente.query.all()
    productos = Producto.query.all()

    return render_template("ventas/form.html", clientes=clientes, productos=productos)