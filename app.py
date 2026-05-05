from flask import Flask, render_template, request, redirect, url_for
from models.db import db
from models.producto import Producto
from models.cliente import Cliente

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tienda.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Proyecto Flask funcionando 🚀"

@app.route("/productos")
def listar():
    productos = Producto.query.all()
    return render_template("productos/index.html", productos=productos)

@app.route("/productos/crear", methods=["GET", "POST"])
def crear_producto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        
        try:
            precio = float(request.form["precio"])
            stock = int(request.form["stock"])
        except ValueError:
            return "Precio y stock deben ser números válidos"

        nuevo = Producto(
            nombre=nombre,
            precio=precio,
            stock=stock
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("listar"))

    return render_template("productos/form.html")

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    producto = db.session.get(Producto, id)

    if not producto:
        return "Producto no encontrado"

    if request.method == "POST":
        producto.nombre = request.form["nombre"]

        try:
            producto.precio = float(request.form["precio"])
            producto.stock = int(request.form["stock"])
        except ValueError:
            return "Precio y stock deben ser números válidos"

        db.session.commit()

        return redirect(url_for("listar"))

    return render_template("productos/form.html", producto=producto)

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    producto = db.session.get(Producto, id)

    if not producto:
        return "Producto no encontrado"

    db.session.delete(producto)
    db.session.commit()

    return redirect(url_for("listar"))

if __name__ == "__main__":
    app.run(debug=True)