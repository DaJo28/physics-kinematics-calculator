import tkinter as tk
from tkinter import ttk, messagebox
from formulas import calcular_mru, calcular_mruv


class CalculadoraFisica:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Física - Cinemática")
        self.root.geometry("980x850")
        self.root.resizable(True, True)
        self.root.configure(bg="#eef3f9")

        self.movimiento_var = tk.StringVar(value="MRU")
        self.objetivo_var = tk.StringVar()

        self.entries = {}
        self.unit_boxes = {}
        self.labels_amigables = {}
        self.campos_requeridos = []
        self.objetivos_map = {}

        self.crear_interfaz()
        self.actualizar_campos()

    def crear_interfaz(self):
        titulo = tk.Label(
            self.root,
            text="Calculadora de Física - Cinemática",
            font=("Comfortaa", 22, "bold"),
            bg="#eef3f9",
            fg="#1f3b5c"
        )
        titulo.pack(pady=(18, 6))

        subtitulo = tk.Label(
            self.root,
            text="Seleccione el tipo de movimiento, el dato que desea calcular, ingrese los valores y elija las unidades.",
            font=("Comfortaa", 10),
            bg="#eef3f9",
            fg="#3b4f63"
        )
        subtitulo.pack(pady=(0, 15))

        marco_seleccion = tk.LabelFrame(
            self.root,
            text="Configuración del problema",
            font=("Comfortaa", 11, "bold"),
            padx=18,
            pady=18,
            bg="white",
            fg="#1f3b5c"
        )
        marco_seleccion.pack(fill="x", padx=20, pady=10)

        tk.Label(
            marco_seleccion,
            text="Tipo de movimiento:",
            font=("Comfortaa", 11),
            bg="white"
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

        combo_movimiento = ttk.Combobox(
            marco_seleccion,
            textvariable=self.movimiento_var,
            values=["MRU", "MRUV"],
            state="readonly",
            width=24
        )
        combo_movimiento.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        combo_movimiento.bind("<<ComboboxSelected>>", lambda e: self.actualizar_campos())

        tk.Label(
            marco_seleccion,
            text="Dato a calcular:",
            font=("Comfortaa", 11),
            bg="white"
        ).grid(row=1, column=0, padx=10, pady=8, sticky="w")

        self.combo_objetivo = ttk.Combobox(
            marco_seleccion,
            textvariable=self.objetivo_var,
            state="readonly",
            width=24
        )
        self.combo_objetivo.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        self.combo_objetivo.bind("<<ComboboxSelected>>", lambda e: self.actualizar_estado_entradas())

        self.marco_campos = tk.LabelFrame(
            self.root,
            text="Datos conocidos y unidades",
            font=("Comfortaa", 11, "bold"),
            padx=18,
            pady=18,
            bg="white",
            fg="#1f3b5c"
        )
        self.marco_campos.pack(fill="x", padx=20, pady=10)

        marco_botones = tk.Frame(self.root, bg="#eef3f9")
        marco_botones.pack(pady=15)

        boton_calcular = tk.Button(
            marco_botones,
            text="Calcular",
            font=("Comfortaa", 12, "bold"),
            bg="#2E86C1",
            fg="white",
            width=16,
            command=self.calcular_resultado
        )
        boton_calcular.grid(row=0, column=0, padx=10)

        boton_limpiar = tk.Button(
            marco_botones,
            text="Limpiar",
            font=("Comfortaa", 12, "bold"),
            bg="#85929e",
            fg="white",
            width=16,
            command=self.limpiar_todo
        )
        boton_limpiar.grid(row=0, column=1, padx=10)

        marco_resultado = tk.LabelFrame(
            self.root,
            text="Resultado",
            font=("Comfortaa", 11, "bold"),
            padx=12,
            pady=12,
            bg="white",
            fg="#1f3b5c"
        )
        marco_resultado.pack(fill="both", expand=True, padx=20, pady=12)

        self.resultado_text = tk.Text(
            marco_resultado,
            font=("Comfortaa", 11),
            bg="white",
            fg="#1b2631",
            wrap="word",
            height=12,
            relief="flat",
            bd=0
        )
        self.resultado_text.pack(fill="both", expand=True)
        self.resultado_text.insert("1.0", "Aquí aparecerá el resultado del cálculo.")
        self.resultado_text.config(state="disabled")

    def limpiar_campos(self):
        for widget in self.marco_campos.winfo_children():
            widget.destroy()
        self.entries.clear()
        self.unit_boxes.clear()
        self.labels_amigables.clear()

    def obtener_unidades_por_variable(self, clave):
        unidades = {
            "distancia": ["m", "km"],
            "velocidad": ["m/s", "km/h"],
            "velocidad_inicial": ["m/s", "km/h"],
            "velocidad_final": ["m/s", "km/h"],
            "tiempo": ["s", "min", "h"],
            "aceleracion": ["m/s²"]
        }
        return unidades.get(clave, [""])

    def actualizar_campos(self):
        self.limpiar_campos()
        movimiento = self.movimiento_var.get()

        if movimiento == "MRU":
            objetivos = [
                ("distancia", "Distancia"),
                ("velocidad", "Velocidad"),
                ("tiempo", "Tiempo")
            ]
            variables = [
                ("distancia", "Distancia"),
                ("velocidad", "Velocidad"),
                ("tiempo", "Tiempo")
            ]
        else:
            objetivos = [
                ("velocidad_final", "Velocidad Final"),
                ("distancia", "Distancia"),
                ("aceleracion", "Aceleración")
            ]
            variables = [
                ("velocidad_inicial", "Velocidad inicial"),
                ("velocidad_final", "Velocidad final"),
                ("aceleracion", "Aceleración"),
                ("tiempo", "Tiempo"),
                ("distancia", "Distancia")
            ]

        self.labels_amigables = {clave: texto for clave, texto in variables}
        self.objetivos_map = {texto: clave for clave, texto in objetivos}

        nombres_objetivos = [texto for _, texto in objetivos]
        self.combo_objetivo["values"] = nombres_objetivos
        self.objetivo_var.set(nombres_objetivos[0])

        tk.Label(
            self.marco_campos,
            text="Magnitud",
            font=("Comfortaa", 11, "bold"),
            bg="white"
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

        tk.Label(
            self.marco_campos,
            text="Valor",
            font=("Comfortaa", 11, "bold"),
            bg="white"
        ).grid(row=0, column=1, padx=10, pady=8, sticky="w")

        tk.Label(
            self.marco_campos,
            text="Unidad",
            font=("Comfortaa", 11, "bold"),
            bg="white"
        ).grid(row=0, column=2, padx=10, pady=8, sticky="w")

        for i, (clave, texto) in enumerate(variables, start=1):
            label = tk.Label(
                self.marco_campos,
                text=f"{texto}:",
                font=("Comfortaa", 11),
                bg="white"
            )
            label.grid(row=i, column=0, padx=12, pady=10, sticky="w")

            entry = tk.Entry(
                self.marco_campos,
                width=20,
                font=("Comfortaa", 11),
                relief="solid",
                bd=1
            )
            entry.grid(row=i, column=1, padx=12, pady=10, sticky="w")

            combo_unidad = ttk.Combobox(
                self.marco_campos,
                values=self.obtener_unidades_por_variable(clave),
                state="readonly",
                width=12
            )
            combo_unidad.grid(row=i, column=2, padx=12, pady=10, sticky="w")
            combo_unidad.set(self.obtener_unidades_por_variable(clave)[0])

            self.entries[clave] = entry
            self.unit_boxes[clave] = combo_unidad

        self.actualizar_estado_entradas()

    def definir_campos_requeridos(self, movimiento, objetivo):
        if movimiento == "MRU":
            requeridos = {
                "distancia": ["velocidad", "tiempo"],
                "velocidad": ["distancia", "tiempo"],
                "tiempo": ["distancia", "velocidad"]
            }
        else:
            requeridos = {
                "velocidad_final": ["velocidad_inicial", "aceleracion", "tiempo"],
                "distancia": ["velocidad_inicial", "aceleracion", "tiempo"],
                "aceleracion": ["velocidad_inicial", "velocidad_final", "tiempo"]
            }
        return requeridos[objetivo]

    def actualizar_estado_entradas(self):
        objetivo_amigable = self.objetivo_var.get()

        if objetivo_amigable not in self.objetivos_map:
            return

        objetivo = self.objetivos_map[objetivo_amigable]
        movimiento = self.movimiento_var.get()
        self.campos_requeridos = self.definir_campos_requeridos(movimiento, objetivo)

        for clave, entry in self.entries.items():
            if clave == objetivo:
                entry.config(state="disabled")
                entry.delete(0, tk.END)
                self.unit_boxes[clave].config(state="readonly")
            elif clave in self.campos_requeridos:
                entry.config(state="normal")
                self.unit_boxes[clave].config(state="readonly")
            else:
                entry.config(state="disabled")
                entry.delete(0, tk.END)
                self.unit_boxes[clave].config(state="disabled")

    def convertir_a_base(self, clave, valor, unidad):
        if clave in ["distancia"]:
            if unidad == "m":
                return valor
            elif unidad == "km":
                return valor * 1000

        elif clave in ["velocidad", "velocidad_inicial", "velocidad_final"]:
            if unidad == "m/s":
                return valor
            elif unidad == "km/h":
                return valor / 3.6

        elif clave == "tiempo":
            if unidad == "s":
                return valor
            elif unidad == "min":
                return valor * 60
            elif unidad == "h":
                return valor * 3600

        elif clave == "aceleracion":
            return valor

        return valor

    def convertir_desde_base(self, clave, valor, unidad):
        if clave == "distancia":
            if unidad == "m":
                return valor
            elif unidad == "km":
                return valor / 1000

        elif clave in ["velocidad", "velocidad_inicial", "velocidad_final"]:
            if unidad == "m/s":
                return valor
            elif unidad == "km/h":
                return valor * 3.6

        elif clave == "tiempo":
            if unidad == "s":
                return valor
            elif unidad == "min":
                return valor / 60
            elif unidad == "h":
                return valor / 3600

        elif clave == "aceleracion":
            return valor

        return valor

    def obtener_datos(self):
        datos = {}

        for clave in self.campos_requeridos:
            valor_texto = self.entries[clave].get().strip()

            if not valor_texto:
                raise ValueError(f"Debe ingresar un valor para {self.labels_amigables[clave]}.")

            try:
                valor = float(valor_texto)
            except ValueError:
                raise ValueError(f"El valor ingresado en {self.labels_amigables[clave]} no es numérico.")

            unidad = self.unit_boxes[clave].get()
            datos[clave] = self.convertir_a_base(clave, valor, unidad)

        return datos

    def formatear_datos_ingresados(self):
        lineas = []
        for clave in self.campos_requeridos:
            valor = self.entries[clave].get().strip()
            unidad = self.unit_boxes[clave].get()
            lineas.append(f"• {self.labels_amigables[clave]} = {valor} {unidad}")
        return "\n".join(lineas)

    def mostrar_resultado(self, texto):
        self.resultado_text.config(state="normal")
        self.resultado_text.delete("1.0", tk.END)
        self.resultado_text.insert("1.0", texto)
        self.resultado_text.config(state="disabled")

    def calcular_resultado(self):
        try:
            movimiento = self.movimiento_var.get()
            objetivo_amigable = self.objetivo_var.get()

            if objetivo_amigable not in self.objetivos_map:
                raise ValueError("Debe seleccionar un dato a calcular.")

            objetivo = self.objetivos_map[objetivo_amigable]
            datos = self.obtener_datos()

            if movimiento == "MRU":
                resultado_base, _ = calcular_mru(objetivo, datos)
            else:
                resultado_base, _ = calcular_mruv(objetivo, datos)

            unidad_salida = self.unit_boxes[objetivo].get()
            resultado_convertido = self.convertir_desde_base(objetivo, resultado_base, unidad_salida)

            texto_resultado = (f"Movimiento seleccionado: {movimiento}\nResultado final: {resultado_convertido:.2f} {unidad_salida}"
            )

            self.mostrar_resultado(texto_resultado)

        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")

    def limpiar_todo(self):
        for clave, entry in self.entries.items():
            entry.config(state="normal")
            entry.delete(0, tk.END)

        for clave, combo in self.unit_boxes.items():
            combo.config(state="readonly")
            combo.set(self.obtener_unidades_por_variable(clave)[0])

        self.actualizar_estado_entradas()
        self.mostrar_resultado("Aquí aparecerá el resultado del cálculo.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraFisica(root)
    root.mainloop()