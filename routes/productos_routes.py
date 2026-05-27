from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.producto import Producto
from models.db import db

producto_bp = Blueprint("producto", __name__)

@producto_bp.route("/productos")
def listar():
    productos = Producto.query.all()
    return render_template("productos/index.html", productos=productos)

@producto_bp.route("/productos/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nombre = request.form["nombre"]

        try:
            precio = float(request.form["precio"])
            stock = int(request.form["stock"])
        except ValueError:
            return "Datos inválidos"

        nuevo = Producto(nombre=nombre, precio=precio, stock=stock)

        db.session.add(nuevo)
        db.session.commit()

        flash("Producto registrado correctamente", "success")

        return redirect(url_for("producto.listar"))

    return render_template("productos/form.html")

@producto_bp.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    producto = db.session.get(Producto, id)

    if not producto:
        return "Producto no encontrado"

    if request.method == "POST":
        producto.nombre = request.form["nombre"]

        try:
            producto.precio = float(request.form["precio"])
            producto.stock = int(request.form["stock"])
        except ValueError:
            return "Datos inválidos"

        db.session.commit()

        flash("Producto modificado correctamente", "success")

        return redirect(url_for("producto.listar"))

    return render_template("productos/form.html", producto=producto)

@producto_bp.route("/productos/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    producto = db.session.get(Producto, id)

    if producto.detalles:
        flash("No se puede eliminar un producto con ventas registradas", "danger")

        return redirect(url_for("producto.listar"))

    if producto:
        db.session.delete(producto)
        db.session.commit()
    
    flash("Producto eliminado correctamente", "success")

    return redirect(url_for("producto.listar"))