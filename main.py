import customtkinter as ctk
from tkinter import messagebox
from formulas import (calcular_mru,calcular_mruv, calcular_caida_libre, calcular_lanzamiento_vertical)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class CalculadoraFisicaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Física - Cinemática")
        self.root.geometry("1180x760")
        self.root.minsize(1080, 700)

        self.movimiento_var = ctk.StringVar(value="MRU")
        self.objetivo_var = ctk.StringVar(value="")

        self.entries = {}
        self.unit_boxes = {}
        self.labels_amigables = {}
        self.campos_requeridos = []
        self.objetivos_map = {}

        self.configurar_grid()
        self.crear_layout()
        self.actualizar_campos()

    def configurar_grid(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

    def crear_layout(self):
        self.header = ctk.CTkFrame(self.root, corner_radius=18, fg_color="#d9e9f7")
        self.header.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=(20, 10))

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Calculadora de Física - Cinemática",
            font=("Comfortaa", 26, "bold"),
            text_color="#16324f"
        )
        self.title_label.pack(pady=(18, 6))

        self.subtitle_label = ctk.CTkLabel(
            self.header,
            text="Seleccione el tipo de movimiento, el dato a calcular, ingrese valores y elija las unidades.",
            font=("Comfortaa", 13),
            text_color="#35516b"
        )
        self.subtitle_label.pack(pady=(0, 18))

        self.panel_izquierdo = ctk.CTkFrame(self.root, corner_radius=18)
        self.panel_izquierdo.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(0, 20))
        self.panel_izquierdo.grid_columnconfigure(0, weight=1)

        self.panel_derecho = ctk.CTkFrame(self.root, corner_radius=18)
        self.panel_derecho.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=(0, 20))
        self.panel_derecho.grid_rowconfigure(1, weight=1)
        self.panel_derecho.grid_columnconfigure(0, weight=1)

        self.crear_panel_configuracion()
        self.crear_panel_resultado()

    def crear_panel_configuracion(self):
        self.config_frame = ctk.CTkFrame(self.panel_izquierdo, corner_radius=14)
        self.config_frame.pack(fill="x", padx=18, pady=(18, 10))

        ctk.CTkLabel(
            self.config_frame,
            text="Configuración del problema",
            font=("Comfortaa", 18, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=18, pady=(18, 16))

        ctk.CTkLabel(
            self.config_frame,
            text="Tipo de movimiento",
            font=("Comfortaa", 13, "bold")
        ).grid(row=1, column=0, sticky="w", padx=18, pady=8)

        self.combo_movimiento = ctk.CTkOptionMenu(
            self.config_frame,
            variable=self.movimiento_var,
            values=["MRU", "MRUV", "CAÍDA LIBRE", "LANZAMIENTO VERTICAL"],
            command=lambda _: self.actualizar_campos(),
            font=("Comfortaa", 12),
            dropdown_font=("Comfortaa", 12)
        )
        self.combo_movimiento.grid(row=1, column=1, sticky="ew", padx=18, pady=8)

        ctk.CTkLabel(
            self.config_frame,
            text="Dato a calcular",
            font=("Comfortaa", 13, "bold")
        ).grid(row=2, column=0, sticky="w", padx=18, pady=(8, 18))

        self.combo_objetivo = ctk.CTkOptionMenu(
            self.config_frame,
            variable=self.objetivo_var,
            values=[""],
            command=lambda _: self.actualizar_estado_entradas(),
            font=("Comfortaa", 12),
            dropdown_font=("Comfortaa", 12)
        )
        self.combo_objetivo.grid(row=2, column=1, sticky="ew", padx=18, pady=(8, 18))

        self.config_frame.grid_columnconfigure(1, weight=1)

        self.datos_frame = ctk.CTkFrame(self.panel_izquierdo, corner_radius=14)
        self.datos_frame.pack(fill="both", expand=True, padx=18, pady=10)
        self.datos_frame.grid_columnconfigure(1, weight=1)

        self.botones_frame = ctk.CTkFrame(self.panel_izquierdo, corner_radius=14)
        self.botones_frame.pack(fill="x", padx=18, pady=(10, 18))

        self.boton_calcular = ctk.CTkButton(
            self.botones_frame,
            text="Calcular",
            command=self.calcular_resultado,
            font=("Comfortaa", 13, "bold"),
            height=42
        )
        self.boton_calcular.pack(side="left", expand=True, fill="x", padx=(16, 8), pady=16)

        self.boton_limpiar = ctk.CTkButton(
            self.botones_frame,
            text="Limpiar",
            command=self.limpiar_todo,
            font=("Comfortaa", 13, "bold"),
            height=42,
            fg_color="#7c8a99",
            hover_color="#6d7985"
        )
        self.boton_limpiar.pack(side="left", expand=True, fill="x", padx=(8, 16), pady=16)

    def crear_panel_resultado(self):
        self.resultado_header = ctk.CTkLabel(
            self.panel_derecho,
            text="Resultado",
            font=("Comfortaa", 18, "bold")
        )
        self.resultado_header.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        self.resultado_text = ctk.CTkTextbox(
            self.panel_derecho,
            font=("Comfortaa", 13),
            corner_radius=14
        )
        self.resultado_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.resultado_text.insert("1.0", "Aquí aparecerá el resultado del cálculo.")
        self.resultado_text.configure(state="disabled")

    def limpiar_campos(self):
        for widget in self.datos_frame.winfo_children():
            widget.destroy()
        self.entries.clear()
        self.unit_boxes.clear()
        self.labels_amigables.clear()

    def obtener_unidades_por_variable(self, clave):
        unidades = {
            "distancia": ["m", "km"],
            "altura": ["m", "km"],
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

        elif movimiento == "MRUV":
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

        elif movimiento == "CAÍDA LIBRE":
            objetivos = [
                ("velocidad", "Velocidad"),
                ("altura", "Altura"),
                ("tiempo", "Tiempo")
            ]
            variables = [
                ("velocidad", "Velocidad"),
                ("altura", "Altura"),
                ("tiempo", "Tiempo")
            ]

        else:  # LANZAMIENTO VERTICAL
            objetivos = [
                ("velocidad_final", "Velocidad Final"),
                ("altura", "Altura"),
                ("tiempo", "Tiempo")
            ]
            variables = [
                ("velocidad_inicial", "Velocidad inicial"),
                ("velocidad_final", "Velocidad final"),
                ("tiempo", "Tiempo"),
                ("altura", "Altura")
            ]

        self.labels_amigables = {clave: texto for clave, texto in variables}
        self.objetivos_map = {texto: clave for clave, texto in objetivos}

        nombres_objetivos = [texto for _, texto in objetivos]
        self.objetivo_var.set(nombres_objetivos[0])
        self.combo_objetivo.configure(values=nombres_objetivos)

        ctk.CTkLabel(
            self.datos_frame,
            text="Datos conocidos y unidades",
            font=("Comfortaa", 18, "bold")
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=18, pady=(18, 12))

        ctk.CTkLabel(
            self.datos_frame,
            text="Magnitud",
            font=("Comfortaa", 12, "bold")
        ).grid(row=1, column=0, padx=18, pady=8, sticky="w")

        ctk.CTkLabel(
            self.datos_frame,
            text="Valor",
            font=("Comfortaa", 12, "bold")
        ).grid(row=1, column=1, padx=18, pady=8, sticky="w")

        ctk.CTkLabel(
            self.datos_frame,
            text="Unidad",
            font=("Comfortaa", 12, "bold")
        ).grid(row=1, column=2, padx=18, pady=8, sticky="w")

        for i, (clave, texto) in enumerate(variables, start=2):
            label = ctk.CTkLabel(
                self.datos_frame,
                text=f"{texto}:",
                font=("Comfortaa", 12)
            )
            label.grid(row=i, column=0, padx=18, pady=10, sticky="w")

            entry = ctk.CTkEntry(
                self.datos_frame,
                font=("Comfortaa", 12),
                placeholder_text="Ingrese valor"
            )
            entry.grid(row=i, column=1, padx=18, pady=10, sticky="ew")

            combo_unidad = ctk.CTkOptionMenu(
                self.datos_frame,
                values=self.obtener_unidades_por_variable(clave),
                font=("Comfortaa", 12),
                dropdown_font=("Comfortaa", 12)
            )
            combo_unidad.grid(row=i, column=2, padx=18, pady=10, sticky="ew")
            combo_unidad.set(self.obtener_unidades_por_variable(clave)[0])

            self.entries[clave] = entry
            self.unit_boxes[clave] = combo_unidad

        self.datos_frame.grid_columnconfigure(1, weight=1)
        self.actualizar_estado_entradas()

    def definir_campos_requeridos(self, movimiento, objetivo):
        if movimiento == "MRU":
            requeridos = {
                "distancia": ["velocidad", "tiempo"],
                "velocidad": ["distancia", "tiempo"],
                "tiempo": ["distancia", "velocidad"]
            }

        elif movimiento == "MRUV":
            requeridos = {
                "velocidad_final": ["velocidad_inicial", "aceleracion", "tiempo"],
                "distancia": ["velocidad_inicial", "aceleracion", "tiempo"],
                "aceleracion": ["velocidad_inicial", "velocidad_final", "tiempo"]
            }

        elif movimiento == "CAÍDA LIBRE":
            requeridos = {
                "velocidad": ["tiempo"],
                "altura": ["tiempo"],
                "tiempo": ["altura"]
            }

        else:  # LANZAMIENTO VERTICAL
            requeridos = {
                "velocidad_final": ["velocidad_inicial", "tiempo"],
                "altura": ["velocidad_inicial", "tiempo"],
                "tiempo": ["velocidad_inicial", "velocidad_final"]
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
                entry.configure(state="disabled")
                entry.delete(0, "end")
                self.unit_boxes[clave].configure(state="normal")
            elif clave in self.campos_requeridos:
                entry.configure(state="normal")
                self.unit_boxes[clave].configure(state="normal")
            else:
                entry.configure(state="disabled")
                entry.delete(0, "end")
                self.unit_boxes[clave].configure(state="disabled")

    def convertir_a_base(self, clave, valor, unidad):
        if clave in ["distancia", "altura"]:
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
        if clave in ["distancia", "altura"]:
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
        self.resultado_text.configure(state="normal")
        self.resultado_text.delete("1.0", "end")
        self.resultado_text.insert("1.0", texto)
        self.resultado_text.configure(state="disabled")

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
            elif movimiento == "MRUV":
                resultado_base, _ = calcular_mruv(objetivo, datos)
            elif movimiento == "CAÍDA LIBRE":
                resultado_base, _ = calcular_caida_libre(objetivo, datos)
            else:
                resultado_base, _ = calcular_lanzamiento_vertical(objetivo, datos)

            unidad_salida = self.unit_boxes[objetivo].get()
            resultado_convertido = self.convertir_desde_base(objetivo, resultado_base, unidad_salida)

            texto_resultado = (
                "Cálculo realizado correctamente\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Movimiento seleccionado: {movimiento}\n"
                f"Dato calculado: {objetivo_amigable}\n\n"
                "Datos ingresados:\n"
                f"{self.formatear_datos_ingresados()}\n\n"
                f"Resultado final: {resultado_convertido:.2f} {unidad_salida}"
            )

            self.mostrar_resultado(texto_resultado)

        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")

    def limpiar_todo(self):
        for clave, entry in self.entries.items():
            entry.configure(state="normal")
            entry.delete(0, "end")

        for clave, combo in self.unit_boxes.items():
            combo.configure(state="normal")
            combo.set(self.obtener_unidades_por_variable(clave)[0])

        self.actualizar_estado_entradas()
        self.mostrar_resultado("Aquí aparecerá el resultado del cálculo.")


if __name__ == "__main__":
    root = ctk.CTk()
    app = CalculadoraFisicaApp(root)
    root.mainloop()