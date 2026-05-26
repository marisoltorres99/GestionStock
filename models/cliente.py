from .db import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50), nullable=True)

    ventas = db.relationship("Venta", back_populates="cliente")

    pagos = db.relationship("Pago", back_populates="cliente")