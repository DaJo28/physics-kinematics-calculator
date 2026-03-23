import tkinter as tk
from tkinter import ttk, messagebox
from formulas import calcular_mru, calcular_mruv

class CalculadoraFisica:
    def __init__(self, root):
        #INTERFAZ INICIAL
        self.root = root
        self.root.title("Calculadora de Física - Cinemática")
        self.root.geometry("760x600")
        self.root.resizable(False, False)
        self.root.configure(bg = "#eef3f9")
        
        self.movimiento_var = tk.StringVar(value = "MRU")
        self.objetivo_var = tk.StringVar()
        
        self.entries = {}
        self.labels_amigables = {}
        
        self.crear_interfaz()
        self.actualizar_campos()
        
    def crear_interfaz(self):
        #Creación de la interfaz gráfica
        # Sección de título
        titulo = tk.Label(self.root, text="Calculadora de Física - Cinemática", font = ("Comfortaa", 20, "bold"), bg = "#eef3f9", fg = "#1f3b5c")
        titulo.pack(pady = (15, 5))
        
        subtitulo = tk.Label(self.root, text = "Seleccione el tipo de movimiento, el dato que desea calcular e ingrese los valores necesarios", font = ("Comfortaa", 10), bg = "#eef3f9", fg = "#3b4f63")
        subtitulo.pack(pady = (0, 15))
        
        #Marco de seleeción
        marco_seleccion = tk.LabelFrame(self.root, text = "Configuración del problema", font = ("Comfortaa", 11, "bold"), padx = 15, pady = 15, bg = "white", fg = "#1f3b5c")
        marco_seleccion.pack(fill = "x", padx = 20, pady = 10)
        
        tk.Label(marco_seleccion, text = "Tipo de movimiento: ", font = ("Comfortaa", 11), bg = "white").grid(row = 0, column = 0, padx = 10, pady = 8, sticky = "w")
        
        combo_movimiento = ttk.Combobox(marco_seleccion, textvariable = self.movimiento_var, values = ["MRU", "MRUV"], state = "readonly", width = 22)
        combo_movimiento.grid(row = 0, column = 1, padx = 10, pady = 8, sticky = "w")
        combo_movimiento.bind("<<ComboboxSelected>>", lambda e: self.actualizar_campos())
        
        tk.Label(marco_seleccion, text = "Dato a calcular: ", font = ("Comfortaa", 11), bg = "white").grid(row = 1, column = 0, padx = 10, pady = 8, sticky = "w")
        
        self.combo_objetivo = ttk.Combobox(marco_seleccion, textvariable = self.objetivo_var, state = "readonly", width = 22)
        self.combo_objetivo.grid(row = 1, column = 1, padx = 10, pady = 8, sticky = "w")
        self.combo_objetivo.bind("<<ComboboxSelected>>", lambda e: self.actualizar_estado_entradas())
        
        #MARCO DE DATOS
        self.marco_campos = tk.LabelFrame(self.root, text = "Datos conocidos", font = ("Comfortaa", 11, "bold"), padx = 15, pady = 15, bg = "white", fg = "#1f3b5c")
        self.marco_campos.pack(fill = "x", padx = 20, pady = 10)
        
        #BOTONES
        marco_botones = tk.Frame(self.root, bg = "#eef3f9")
        marco_botones.pack(pady = 15)
        
        boton_calcular = tk.Button(marco_botones, text = "Calcular", font = ("Comfortaa", 12, "bold"), bg = "#2E86C1", fg = "white", width = 15, command = self.calcular_resultado)
        boton_calcular.grid(row = 0, column = 0, padx = 10)
        
        boton_limpiar = tk.Button(marco_botones, text = "Limpiar", font = ("Comfortaa", 12, "bold"), bg = "#85929e", fg = "white", width = 15, command = self.limpiar_todo)
        boton_limpiar.grid(row = 0, column = 1, padx = 10)
        
        #RESULTADO
        marco_resultado = tk.LabelFrame(self.root, text = "Resultado", font = ("Comfortaa", 11, "bold"), padx = 15, pady = 15, bg = "white", fg = "#1f3b5c")
        marco_resultado.pack(fill = "both", expand = True, padx = 20, pady = 10)
        
        self.resultado_label = tk.Label(marco_resultado, text = "Aquí aparecerá el resultado del cálculo.", font = ("Comfortaa", 14, "bold"), bg = "white", fg = "#1b2631", wraplength = 650, justify = "left")
        self.resultado_label.pack(anchor = "w")
        
    def limpiar_campos(self):
        #Limpiar los campos de entrada y el resultado
        for widget in self.marco_campos.winfo_children():
            widget.destroy()
        self.entries.clear()
        self.labels_amigables.clear()
        
    def actualizar_campos(self):
        #Actualizar los campos de entrada según el tipo de movimiento seleccionado
        self.limpiar_campos()
        movimiento = self.movimiento_var.get()
        
        if movimiento == "MRU":
            #Definir los objetivos y variables para MRU
            objetivos = [("distancia", "Distancia"), ("velocidad", "Velocidad"), ("tiempo", "Tiempo")]
            variables = [("distancia", "Distancia (m): "), ("velocidad", "Velocidad (m/s): "), ("tiempo", "Tiempo (s): ")]
        else:
            #Definir los objetivos y variables para MRUV
            objetivos = [("velocidad_final", "Velocidad Final"), ("distancia", "Distancia"), ("aceleracion", "Aceleración")]
            variables = [("velocidad_inicial", "Velocidad inicial (m/s): "), ("velocidad_final", "Velocidad final (m/s): "), ("aceleracion", "Aceleración (m/s²): "), ("tiempo", "Tiempo (s): "), ("distancia", "Distancia (m): ")]
            
        #GUARDAR LAS ETIQUETAS AMIGABLES PARA USAR EN LOS MENSAJES DE ERROR
        self.labels_amigables = {clave: texto.replace(":", "") for clave, texto in variables}
        
        #OBJETIVO AMIGABLES EN EL COMBOBOX
        self.objetivos_map = {texto: clave for clave, texto in objetivos}
        nombres_objetivos = [texto for _, texto in objetivos]
        
        self.combo_objetivo["values"] = nombres_objetivos
        self.objetivo_var.set(nombres_objetivos[0])
        
        for i, (clave, texto) in enumerate(variables):
            #Crear etiquetas y campos de entrada para cada variable
            label = tk.Label(self.marco_campos, text = texto, font = ("Comfortaa", 11), bg = "white")
            label.grid(row = i, column = 0, padx = 12, pady = 8, sticky = "w")
            
            #Crear campo de entrada para cada variable
            entry = tk.Entry(self.marco_campos, width = 25, font = ("Comfortaa", 11), relief = "solid", bd = 1)
            entry.grid(row = i, column = 1, padx = 12, pady = 8, sticky = "w")
            
            self.entries[clave] = entry
        
        self.actualizar_estado_entradas()
        
    def actualizar_estado_entradas(self):
        #Habilitar o deshabilitar campos de entrada según el objetivo seleccionado
        objetivo_amigable = self.objetivo_var.get()
        objetivo = self.objetivos_map[objetivo_amigable]
        
        for clave, entry in self.entries.items():
            if clave == objetivo:
                #Deshabilitar el campo de entrada para la variable objetivo
                entry.config(state = "disabled")
                entry.delete(0, tk.END)
            else:
                #Habilitar los campos de entrada para las variables necesarias
                entry.config(state = "normal")
    
    def obtener_datos(self):
        #Obtener los datos ingresados por el usuario y convertirlos a float, asegurándose de que los campos necesarios estén completos
        datos = {}
        objetivo_amigable = self.objetivo_var.get()
        objetivo = self.objetivos_map[objetivo_amigable]
        
        #Recorrer los campos de entrada y obtener los valores, verificando que los campos necesarios estén completos
        for clave, entry in self.entries.items():
            #Solo obtener el valor de los campos que están habilitados (no son el objetivo)
            if clave != objetivo:
                valor_texto = entry.get().strip()
                if not valor_texto:
                    #Si el campo está vacío, mostrar un mensaje de error indicando qué variable falta
                    nombre_visible = self.labels_amigables.get(clave, clave)
                    raise ValueError(f"Debe ingresar un valor para {nombre_visible}.")
                
                try:
                    datos[clave] = float(valor_texto)
                except ValueError as e:
                    nombre_visible = self.labels_amigables.get(clave, clave)
                    raise ValueError(f"El valor ingresado en {nombre_visible} no es un número válido.") from e
        
        return datos, objetivo
    
    def calcular_resultado(self):
        try:
            #Obtener el tipo de movimiento, el objetivo a calcular y los datos ingresados por el usuario
            movimiento = self.movimiento_var.get()
            datos, objetivo = self.obtener_datos()
            
            if movimiento == "MRU":
                resultado, unidad = calcular_mru(objetivo, datos)
            else:
                resultado, unidad = calcular_mruv(objetivo, datos)
            
            #Mostrar el resultado en la etiqueta correspondiente, formateando el número a 2 decimales y mostrando la unidad de medida
            nombre_objetivo = self.objetivo_var.get()
            self.resultado_label.config(text = (f"Movimiento: {movimiento}\n"
                                                f"Dato Calculado: {nombre_objetivo}\n"
                                                f"Resultado: {resultado:.2f} {unidad}"))
        except ValueError as e:
            #Mostrar un mensaje de error si ocurre una excepción de valor, como campos vacíos o datos no numéricos
            messagebox.showerror("Error de entrada", str(e))
        except Exception:
            #Mostrar un mensaje de error genérico para cualquier otra excepción inesperada
            messagebox.showerror("Error", "Ocurrió un error inesperado. Verifica tus datos e intenta nuevamente.")
            
    def limpiar_todo(self):
        for entry in self.entries.values():
            entry.config(state = "normal")
            entry.delete(0, tk.END)
        
        self.actualizar_estado_entradas()
        self.resultado_label.config(text = "Aquí aparecerá el resultado del cálculo")
    
if __name__ == "__main__":
    #Crear la ventana principal y ejecutar la aplicación
    root = tk.Tk()
    app = CalculadoraFisica(root)
    #Iniciar el bucle principal de la interfaz gráfica
    root.mainloop()
            