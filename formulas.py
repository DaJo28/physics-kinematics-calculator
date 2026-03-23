#File to work on the logic of the formulas and calculations
def calcular_mru(objetivo, datos):
    #Distancia (float) = Velocidad * Tiempo
    #Velocidad (float) = Distancia / Tiempo
    #Tiempo (float) = Distancia / Velocidad
    if (objetivo == "distancia"):
        return datos["velocidad"] * datos["tiempo"], "m"
    
    elif (objetivo == "velocidad"):
        if datos["tiempo"] == 0:
            raise ValueError("El tiempo no puede ser 0.")
        return datos["distancia"] / datos["tiempo"], "m/s"
    
    elif (objetivo == "tiempo"):
        if (datos["velocidad"] == 0):
            raise ValueError("La velocidad no puede ser cero para calcular el tiempo.")
        return datos["distancia"] / datos["velocidad"], "s"
    
    raise ValueError("Variable objetivo no válida. Debe ser 'distancia', 'velocidad' o 'tiempo'.")
    
def calcular_mruv(objetivo, datos):
    #Velocidad Final (float) = Velocidad Inicial + (Aceleración * Tiempo)
    #Distancia (float) = (Velocidad Inicial * Tiempo) + (0.5 * Aceleración * Tiempo^2)
    #Aceleración (float) = (Velocidad Final - Velocidad Inicial) / Tiempo
    if (objetivo == "velocidad_final"):
        return datos["velocidad_inicial"] + (datos["aceleracion"] * datos["tiempo"]), "m/s"
    
    elif (objetivo == "distancia"):
        return ((datos["velocidad_inicial"] * datos["tiempo"]) + (0.5 * datos["aceleracion"] * (datos["tiempo"]**2))), "m"
    
    elif (objetivo == "aceleracion"):
        if (datos["tiempo"] == 0):
            raise ValueError("El tiempo no puede ser cero para calcular la aceleración.")
        return (datos["velocidad_final"] - datos["velocidad_inicial"]) / datos["tiempo"], "m/s²"
    
    raise ValueError("Variable objetivo no válida. Debe ser 'velocidad_final', 'distancia' o 'aceleracion'.")