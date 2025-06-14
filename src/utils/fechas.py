from datetime import datetime
def formatear_fecha(fecha: datetime) -> str:
    return fecha.strftime("%d/%m/%Y")