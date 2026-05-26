from models.db import db
from datetime import datetime

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    tipo_pago = db.Column(db.String(20), nullable=False, server_default='efectivo')

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=True)

    detalles = db.relationship("DetalleVenta", backref="venta", lazy=True)

    cliente = db.relationship("Cliente", back_populates="ventas")