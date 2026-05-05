from flask import Blueprint, render_template, request, redirect, url_for
from models.cliente import Cliente
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

    if cliente:
        db.session.delete(cliente)
        db.session.commit()

    return redirect(url_for("cliente.listar"))