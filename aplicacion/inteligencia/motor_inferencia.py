def evaluar_evento(tipo_evento: str) -> dict:
    t = (tipo_evento or "").strip().upper()

    reglas = {
        "EXCESO_VELOCIDAD": ("ALTA", "Notificar supervisor y registrar evidencia"),
        "DESVIO_RUTA": ("ALTA", "Verificar GPS, contactar operador, posible incidente"),
        "PARADA_NO_PROGRAMADA": ("MEDIA", "Validar motivo de parada y zona"),
        "BAJA_COMBUSTIBLE": ("BAJA", "Sugerir repostaje y recalcular ruta"),
        "MANTENIMIENTO": ("BAJA", "Programar revisión preventiva"),
    }

    severidad, accion = reglas.get(
        t, ("MEDIA", "Registrar evento y solicitar validación manual")
    )

    return {"tipo_evento": t, "severidad": severidad, "accion_sugerida": accion}