from models.db import db

class DetalleVenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    venta_id = db.Column(db.Integer, db.ForeignKey("venta.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("producto.id"), nullable=False)

    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)