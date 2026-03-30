# File to work on the logic of the formulas and calculations

def calcular_mru(objetivo, datos):
    if objetivo == "distancia":
        resultado = datos["velocidad"] * datos["tiempo"]
        procedimiento = (f"Ecuación aplicada: d = v * t\nd = ({datos["velocidad"]:.2f} m/s) * ({datos["tiempo"]:.2f} s)\nd = {resultado:.2f} m")
        return resultado, "m", procedimiento

    elif objetivo == "velocidad":
        if datos["tiempo"] == 0:
            raise ValueError("El tiempo no puede ser 0.")
        resultado = datos["distancia"] / datos["tiempo"]
        procedimiento = (f"Ecuación aplicada: v = d / t\nv = ({datos["distancia"]:.2f} m) / ({datos["tiempo"]:.2f} s)\nv = {resultado:.2f} m/s")
        return resultado, "m/s", procedimiento

    elif objetivo == "tiempo":
        if datos["velocidad"] == 0:
            raise ValueError("La velocidad no puede ser cero para calcular el tiempo.")
        resultado = datos["distancia"] / datos["velocidad"]
        procedimiento = (f"Ecuación aplicada: t = d / v\nt = ({datos["distancia"]:.2f} m) / ({datos["velocidad"]:.2f} m/s)\nt = {resultado:.2f} s")
        return resultado, "s", procedimiento

    raise ValueError("Variable objetivo no válida. Debe ser 'distancia', 'velocidad' o 'tiempo'.")


def calcular_mruv(objetivo, datos):
    if objetivo == "velocidad_final":
        return datos["velocidad_inicial"] + (datos["aceleracion"] * datos["tiempo"]), "m/s"

    elif objetivo == "distancia":
        return (
            (datos["velocidad_inicial"] * datos["tiempo"]) +
            (0.5 * datos["aceleracion"] * (datos["tiempo"] ** 2)),
            "m"
        )

    elif objetivo == "aceleracion":
        if datos["tiempo"] == 0:
            raise ValueError("El tiempo no puede ser cero para calcular la aceleración.")
        return (datos["velocidad_final"] - datos["velocidad_inicial"]) / datos["tiempo"], "m/s²"

    raise ValueError("Variable objetivo no válida. Debe ser 'velocidad_final', 'distancia' o 'aceleracion'.")

def calcular_caida_libre(objetivo, datos):
    g = 9.8 #es el valor de la gravedad
    
    if objetivo == "velocidad":
        return (g * datos["tiempo"], "m/s")
    
    elif objetivo == "altura":
        return (0.5 * g * (datos["tiempo"] ** 2), "m")
    
    elif objetivo == "tiempo":
        if datos["altura"] < 0:
            raise ValueError("La altura no puede ser negativa para calcular el tiempo de caída libre.")
        return (((2 * datos["altura"])/g)**0.5, "s")
    
    raise ValueError("Variable objetivo no válida para caída libre.")

def calcular_lanzamiento_vertical(objetivo, datos):
    g = 9.8 #es el valor de la gravedad

    if objetivo == "velocidad_final":
        return datos["velocidad_inicial"] - (g * datos["tiempo"]), "m/s"

    elif objetivo == "altura":
        return (
            (datos["velocidad_inicial"] * datos["tiempo"]) -
            (0.5 * g * (datos["tiempo"] ** 2)),
            "m"
        )

    elif objetivo == "tiempo":
        if datos["velocidad_inicial"] < 0:
            raise ValueError("La velocidad inicial no puede ser negativa para calcular el tiempo.")
        return ((datos["velocidad_inicial"] - datos["velocidad_final"]) / g, "s")

    raise ValueError("Variable objetivo no válida. Debe ser 'velocidad_final', 'altura' o 'tiempo'.")