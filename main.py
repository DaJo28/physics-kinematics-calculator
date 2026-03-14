import tkinter as tk
from tkinter import ttk, messagebox
from formulas import calcular_mru, calcular_mruv

class CalculadoraFisica:
    def __init__(self, root):
        #INTERFAZ INICIAL
        self.root = root
        self.root.title("Calculadora de Física - Cinemática")
        self.root.geometry("650x520")
        self.root.resizable(False, False)
        
        self.movimiento_var = tk.StringVar(value = "MRU")
        self.objetivo_var = tk.StringVar()
        
        self.entries = {}
        
        self.crear_interfaz()
        self.actualizar_campos()
        
    def crear_interfaz(self):
        #Creación de la interfaz gráfica
        # Sección de título
        titulo = tk.Label(self.root, text="Calculadora de Física - Cinemática", font = ("Comfortaa", 18, "bold"))
        titulo.pack(pady = 15)
        
        marco_superior = tk.Frame(self.root)
        marco_superior.pack(pady = 10)
        
        # Sección de selección de movimiento y variable a calcular
        tk.Label(marco_superior, text = "Tipo de Movimiento: ", font = ("Comfortaa", 11)).grid(row = 0, column = 0, padx = 5, pady = 5)
        combo_movimiento = ttk.Combobox(marco_superior, textvariable = self.movimiento_var, values = ["MRU", "MRUV"], state = "readonly", width = 20)
        combo_movimiento.grid(row = 0, column = 1, padx = 5, pady = 5)
        combo_movimiento.bind("<<ComboboxSelected>>", lambda e: self.actualizar_campos())
        
        tk.Label(marco_superior, text = "Dato a calcular: ", font = ("Comfortaa", 11)).grid(row = 1, column = 0, padx = 5, pady = 5)
        self.combo_objetivo = ttk.Combobox(marco_superior, textvariable = self.objetivo_var, state = "readonly", width = 20)
        self.combo_objetivo.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.combo_objetivo.bind("<<ComboboxSelected>>", lambda e: self.actualizar_estado_entradas())
        
        # Sección de ingreso de datos
        self.marco_campos = tk.LabelFrame(self.root, text = "Ingreso de datos: ", font = ("Comfortaa", 8) ,padx = 15, pady = 15)
        self.marco_campos.pack(padx = 20, pady = 15, fill = "x")
        
        self.boton_calcular = tk.Button(self.root, text = "Calcular", font = ("Comfortaa", 12, "bold"), bg = "#2E86C1", fg = "white", command = self.calcular_resultado)
        self.boton_calcular.pack(pady = 10)
        
        self.resultado_label = tk.Label(self.root, text = "Resultado: ", font = ("Comfortaa", 13, "bold"), fg = "#1B2631")
        self.resultado_label.pack(pady = 15)
        
    def limpiar_campos(self):
        #Limpiar los campos de entrada y el resultado
        for widget in self.marco_campos.winfo_children():
            widget.destroy()
        self.entries.clear()
        
    def actualizar_campos(self):
        #Actualizar los campos de entrada según el tipo de movimiento seleccionado
        self.limpiar_campos()
        movimiento = self.movimiento_var.get()
        
        if movimiento == "MRU":
            #Definir los objetivos y variables para MRU
            objetivos = ["distancia", "velocidad", "tiempo"]
            variables = [("distancia", "Distancia (m): "), ("velocidad", "Velocidad (m/s): "), ("tiempo", "Tiempo (s): ")]
        else:
            #Definir los objetivos y variables para MRUV
            objetivos = ["velocidad_final", "distancia", "aceleracion"]
            variables = [("velocidad_inicial", "Velocidad inicial (m/s): "), ("velocidad_final", "Velocidad final (m/s): "), ("aceleracion", "Aceleración (m/s²): "), ("tiempo", "Tiempo (s): "), ("distancia", "Distancia (m): ")]
        
        #Actualizar las opciones del combo de objetivo
        self.combo_objetivo["values"] = objetivos
        self.objetivo_var.set(objetivos[0])
        
        for i, (clave, texto) in enumerate(variables):
            #Crear etiquetas y campos de entrada para cada variable
            label = tk.Label(self.marco_campos, text = texto, font = ("Comfortaa", 11))
            label.grid(row = i, column = 0, sticky = "w", padx = 10, pady = 6)
            
            #Crear campo de entrada para cada variable
            entry = tk.Entry(self.marco_campos, width = 25, font = ("Comfortaa", 11))
            entry.grid(row = i, column = 1, padx = 10, pady = 6)
            
            self.entries[clave] = entry
        
        self.actualizar_estado_entradas()
        
    def actualizar_estado_entradas(self):
        #Habilitar o deshabilitar campos de entrada según el objetivo seleccionado
        objetivo = self.objetivo_var.get()
        
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
        #Recorrer los campos de entrada y obtener los valores, verificando que los campos necesarios estén completos
        for clave, entry in self.entries.items():
            #Solo obtener el valor de los campos que están habilitados (no son el objetivo)
            if entry["state"] == "normal":
                valor_texto = entry.get().strip()
                if not valor_texto:
                    #Si el campo está vacío, mostrar un error indicando que se debe ingresar el valor
                    raise ValueError(f"Debes ingresar el valor de {clave}.")
                datos[clave] = float(valor_texto)
        return datos
    
    def calcular_resultado(self):
        try:
            #Obtener el tipo de movimiento, el objetivo a calcular y los datos ingresados por el usuario
            movimiento = self.movimiento_var.get()
            objetivo = self.objetivo_var.get()
            datos = self.obtener_datos()
            
            if movimiento == "MRU":
                resultado, unidad = calcular_mru(objetivo, datos)
            else:
                resultado, unidad = calcular_mruv(objetivo, datos)
            
            #Mostrar el resultado en la etiqueta correspondiente, formateando el número a 2 decimales y mostrando la unidad de medida
            self.resultado_label.config(text = f"Resultado: {objetivo} = {resultado:.2f} {unidad}")
        except ValueError as e:
            #Mostrar un mensaje de error si ocurre una excepción de valor, como campos vacíos o datos no numéricos
            messagebox.showerror("Error", str(e))
        except Exception:
            #Mostrar un mensaje de error genérico para cualquier otra excepción inesperada
            messagebox.showerror("Error", "Ocurrió un error inesperado. Verifica tus datos e intenta nuevamente.")
    
if __name__ == "__main__":
    #Crear la ventana principal y ejecutar la aplicación
    root = tk.Tk()
    app = CalculadoraFisica(root)
    #Iniciar el bucle principal de la interfaz gráfica
    root.mainloop()
            