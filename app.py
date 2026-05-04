from flask import Flask, render_template
from models.Producto import Producto
from models.Producto import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///productos.db"
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

if __name__ == "__main__":
    app.run(debug=True)