from models.db import db
from models.venta import Venta
from models.pago import Pago
from sqlalchemy import func

def calcular_deuda_cliente(id):
    
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

    return monto_ventas_fiadas, monto_pagos, deuda
