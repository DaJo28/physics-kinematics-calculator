import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from formulas import (
    calcular_mru,
    calcular_mruv,
    calcular_caida_libre,
    calcular_lanzamiento_vertical
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class CalculadoraFisicaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kadimy's Calculator")
        self.root.geometry("1050x700")
        self.root.minsize(900, 620)
        self.root.resizable(True, True)

        self.movimiento_var = ctk.StringVar(value="MRU")
        self.objetivo_var = ctk.StringVar(value="")
        self.tema_var = ctk.StringVar(value = "Claro")

        self.entries = {}
        self.unit_boxes = {}
        self.labels_amigables = {}
        self.campos_requeridos = []
        self.objetivos_map = {}
        self.historial = []
        self.ultimo_calculo = None
        self.canvas_grafico = None

        self.configurar_grid()
        self.crear_layout()
        self.actualizar_campos()

    def configurar_grid(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)

    def crear_layout(self):
        self.header = ctk.CTkFrame(self.root, corner_radius=18, fg_color="#d9e9f7")
        self.header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Kadimy's Calculator",
            font=("Comfortaa", 24, "bold"),
            text_color="#16324f"
        )
        self.title_label.pack(pady=(14, 4))

        self.subtitle_label = ctk.CTkLabel(
            self.header,
            text="Seleccione un tipo de movimiento, resuelva ejercicios y genere gráficas.",
            font=("Comfortaa", 12),
            text_color="#35516b"
        )
        self.subtitle_label.pack(pady=(0, 14))
        
        self.tema_frame = ctk.CTkFrame(self.header, fg_color = "transparent")
        self.tema_frame.pack(pady = (0, 14))
        
        self.tema_label = ctk.CTkLabel(self.tema_frame, text = "Tema: ", font = ("Comfortaa", 12, "bold"), text_color = "#35516b")
        self.tema_label.pack(side = "left", padx = (0, 10))
        
        self.tema_selector = ctk.CTkSegmentedButton(self.tema_frame, values = ["Claro", "Oscuro"], variable = self.tema_var, command = self.cambiar_tema, font = ("Comfortaa", 12))
        self.tema_selector.pack(side = "left")
        self.tema_selector.set("Claro")

        self.tabs = ctk.CTkTabview(self.root, corner_radius=18)
        self.tabs.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))

        self.tab_inicio = self.tabs.add("Inicio")
        self.tab_calculadora = self.tabs.add("Calculadora")
        self.tab_grafica = self.tabs.add("Gráfica")
        self.tab_historial = self.tabs.add("Historial")

        self.crear_tab_inicio()
        self.crear_tab_calculadora()
        self.crear_tab_grafica()
        self.crear_tab_historial()

        self.tabs.set("Inicio")

    def crear_tab_inicio(self):
        for col in range(2):
            self.tab_inicio.grid_columnconfigure(col, weight=1)
        for row in range(2):
            self.tab_inicio.grid_rowconfigure(row, weight=1)

        movimientos = [
            ("MRU", "Movimiento rectilíneo uniforme: velocidad constante."),
            ("MRUV", "Movimiento rectilíneo uniformemente variado: aceleración constante."),
            ("CAÍDA LIBRE", "Movimiento vertical bajo la acción de la gravedad."),
            ("LANZAMIENTO VERTICAL", "Movimiento vertical con velocidad inicial y gravedad.")
        ]

        for index, (movimiento, descripcion) in enumerate(movimientos):
            fila = index // 2
            columna = index % 2

            card = ctk.CTkFrame(self.tab_inicio, corner_radius=18)
            card.grid(row=fila, column=columna, sticky="nsew", padx=16, pady=16)

            titulo = ctk.CTkLabel(
                card,
                text=movimiento,
                font=("Comfortaa", 20, "bold")
            )
            titulo.pack(pady=(28, 8))

            texto = ctk.CTkLabel(
                card,
                text=descripcion,
                font=("Comfortaa", 12),
                wraplength=360
            )
            texto.pack(pady=(0, 22), padx=20)

            boton = ctk.CTkButton(
                card,
                text="Seleccionar movimiento",
                font=("Comfortaa", 13, "bold"),
                height=40,
                command=lambda m=movimiento: self.seleccionar_movimiento_desde_menu(m)
            )
            boton.pack(pady=(0, 28), padx=24, fill="x")

    def seleccionar_movimiento_desde_menu(self, movimiento):
        self.movimiento_var.set(movimiento)
        self.actualizar_campos()
        self.tabs.set("Calculadora")

    def crear_tab_calculadora(self):
        self.tab_calculadora.grid_columnconfigure(0, weight=1)
        self.tab_calculadora.grid_columnconfigure(1, weight=2)
        self.tab_calculadora.grid_rowconfigure(0, weight=1)

        self.panel_izquierdo = ctk.CTkFrame(self.tab_calculadora, corner_radius=18)
        self.panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=(12, 8), pady=12)
        self.panel_izquierdo.grid_columnconfigure(0, weight=1)

        self.panel_derecho = ctk.CTkFrame(self.tab_calculadora, corner_radius=18)
        self.panel_derecho.grid(row=0, column=1, sticky="nsew", padx=(8, 12), pady=12)
        self.panel_derecho.grid_rowconfigure(1, weight=1)
        self.panel_derecho.grid_columnconfigure(0, weight=1)

        self.crear_panel_configuracion()
        self.crear_panel_resultado()

    def crear_panel_configuracion(self):
        self.panel_izquierdo.grid_rowconfigure(0, weight=0)
        self.panel_izquierdo.grid_rowconfigure(1, weight=1)
        self.panel_izquierdo.grid_rowconfigure(2, weight=0)
        self.panel_izquierdo.grid_columnconfigure(0, weight=1)

        self.config_frame = ctk.CTkFrame(self.panel_izquierdo, corner_radius=14)
        self.config_frame.grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 8))
        self.config_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.config_frame,
            text="Configuración del cálculo",
            font=("Comfortaa", 17, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16, 12))

        ctk.CTkLabel(
            self.config_frame,
            text="Tipo de movimiento:",
            font=("Comfortaa", 12, "bold")
        ).grid(row=1, column=0, sticky="w", padx=16, pady=6)

        self.combo_movimiento = ctk.CTkOptionMenu(
            self.config_frame,
            variable=self.movimiento_var,
            values=["MRU", "MRUV", "CAÍDA LIBRE", "LANZAMIENTO VERTICAL"],
            command=lambda _: self.actualizar_campos(),
            font=("Comfortaa", 12),
            dropdown_font=("Comfortaa", 12)
        )
        self.combo_movimiento.grid(row=1, column=1, sticky="ew", padx=16, pady=6)

        ctk.CTkLabel(
            self.config_frame,
            text="Dato a calcular:",
            font=("Comfortaa", 12, "bold")
        ).grid(row=2, column=0, sticky="w", padx=16, pady=(6, 16))

        self.combo_objetivo = ctk.CTkOptionMenu(
            self.config_frame,
            variable=self.objetivo_var,
            values=[""],
            command=lambda _: self.actualizar_estado_entradas(),
            font=("Comfortaa", 12),
            dropdown_font=("Comfortaa", 12)
        )
        self.combo_objetivo.grid(row=2, column=1, sticky="ew", padx=16, pady=(6, 16))

        self.datos_frame = ctk.CTkScrollableFrame(self.panel_izquierdo, corner_radius=14)
        self.datos_frame.grid(row=1, column=0, sticky="nsew", padx=14, pady=8)
        self.datos_frame.grid_columnconfigure(1, weight=1)

        self.botones_frame = ctk.CTkFrame(self.panel_izquierdo, corner_radius=14)
        self.botones_frame.grid(row=2, column=0, sticky="ew", padx=14, pady=(8, 14))

        self.boton_calcular = ctk.CTkButton(
            self.botones_frame,
            text="Calcular",
            command=self.calcular_resultado,
            font=("Comfortaa", 12, "bold"),
            height=38
        )
        self.boton_calcular.grid(row=0, column=0, sticky="ew", padx=(12, 6), pady=12)

        self.boton_graficar = ctk.CTkButton(
            self.botones_frame,
            text="Graficar",
            command=self.generar_grafico,
            font=("Comfortaa", 12, "bold"),
            height=38,
            fg_color="#2471a3",
            hover_color="#1f618d"
        )
        self.boton_graficar.grid(row=0, column=1, sticky="ew", padx=6, pady=12)

        self.boton_limpiar = ctk.CTkButton(
            self.botones_frame,
            text="Limpiar",
            command=self.limpiar_todo,
            font=("Comfortaa", 12, "bold"),
            height=38,
            fg_color="#7c8a99",
            hover_color="#6d7985"
        )
        self.boton_limpiar.grid(row=0, column=2, sticky="ew", padx=(6, 12), pady=12)

        for col in range(3):
            self.botones_frame.grid_columnconfigure(col, weight=1)

    def crear_panel_resultado(self):
        self.resultado_header = ctk.CTkLabel(
            self.panel_derecho,
            text="Resultado",
            font=("Comfortaa", 18, "bold")
        )
        self.resultado_header.grid(row=0, column=0, sticky="w", padx=18, pady=(18, 10))

        self.resultado_text = ctk.CTkTextbox(
            self.panel_derecho,
            font=("Comfortaa", 12),
            corner_radius=14
        )
        self.resultado_text.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self.resultado_text.insert("1.0", "Aquí aparecerá el resultado del cálculo.")
        self.resultado_text.configure(state="disabled")
        
        self.resultado_botones_frame = ctk.CTkFrame(self.panel_derecho, corner_radius = 14)
        self.resultado_botones_frame.grid(row = 2, column = 0, sticky = "ew", padx = 18, pady = (0, 18))
        self.boton_exportar_resultado = ctk.CTkButton(self.resultado_botones_frame, text = "Exportar resultado a TXT", command = self.exportar_resultado_txt, font = ("Comfortaa", 12, "bold"), height = 38, fg_color = "#229954", hover_color = "#1e8449")
        self.boton_exportar_resultado.pack(fill = "x", padx = 12, pady = 12)

    def crear_tab_grafica(self):
        self.tab_grafica.grid_columnconfigure(0, weight=1)
        self.tab_grafica.grid_rowconfigure(1, weight=1)

        titulo = ctk.CTkLabel(
            self.tab_grafica,
            text="Gráfica del movimiento",
            font=("Comfortaa", 20, "bold")
        )
        titulo.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        self.grafico_frame = ctk.CTkFrame(self.tab_grafica, corner_radius=14)
        self.grafico_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 15))

        self.boton_graficar_tab = ctk.CTkButton(
            self.tab_grafica,
            text="Generar gráfico del último cálculo",
            command=self.generar_grafico,
            font=("Comfortaa", 12, "bold")
        )
        self.boton_graficar_tab.grid(row=2, column=0, pady=(0, 20))

    def crear_tab_historial(self):
        self.tab_historial.grid_columnconfigure(0, weight=1)
        self.tab_historial.grid_rowconfigure(1, weight=1)

        titulo = ctk.CTkLabel(
            self.tab_historial,
            text="Historial de cálculos",
            font=("Comfortaa", 20, "bold")
        )
        titulo.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        self.historial_text = ctk.CTkTextbox(
            self.tab_historial,
            font=("Comfortaa", 12),
            corner_radius=14
        )
        self.historial_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 15))
        self.historial_text.configure(state="disabled")

        self.historial_botones_frame = ctk.CTkFrame(self.tab_historial, corner_radius = 14)
        self.historial_botones_frame.grid(row = 2, column = 0, sticky = "ew", padx = 20, pady = (0, 20))
        
        self.boton_exportar_historial = ctk.CTkButton(self.historial_botones_frame, text = "Exportar historial a TXT", command = self.exportar_historial_txt, font = ("Comfortaa", 12, "bold"), fg_color = "#229954", hover_color = "#1e8449")
        self.boton_exportar_historial.grid(row = 0, column = 0, sticky = "ew", padx = (12, 6), pady = 12)
        
        self.boton_limpiar_historial = ctk.CTkButton(self.historial_botones_frame, text = "Limpiar historial", command = self.limpiar_historial, font = ("Comfortaa", 12, "bold"), fg_color = "#c0392b", hover_color = "#a93226")
        self.boton_limpiar_historial.grid(row = 0, column = 1, sticky = "ew", padx = (6, 12), pady = 12)
        
        self.historial_botones_frame.grid_columnconfigure(0, weight = 1)
        self.historial_botones_frame.grid_columnconfigure(1, weight = 1)

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

        else:
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
            font=("Comfortaa", 16, "bold")
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=14, pady=(10, 8))

        ctk.CTkLabel(
            self.datos_frame,
            text="Magnitud",
            font=("Comfortaa", 12, "bold")
        ).grid(row=1, column=0, padx=14, pady=6, sticky="w")

        ctk.CTkLabel(
            self.datos_frame,
            text="Valor",
            font=("Comfortaa", 12, "bold")
        ).grid(row=1, column=1, padx=14, pady=6, sticky="w")

        ctk.CTkLabel(
            self.datos_frame,
            text="Unidad",
            font=("Comfortaa", 12, "bold")
        ).grid(row=1, column=2, padx=14, pady=6, sticky="w")

        for i, (clave, texto) in enumerate(variables, start=2):
            label = ctk.CTkLabel(
                self.datos_frame,
                text=f"{texto}:",
                font=("Comfortaa", 12)
            )
            label.grid(row=i, column=0, padx=14, pady=5, sticky="w")

            entry = ctk.CTkEntry(
                self.datos_frame,
                font=("Comfortaa", 12),
                placeholder_text="Ingrese valor"
            )
            entry.grid(row=i, column=1, padx=14, pady=5, sticky="ew")

            combo_unidad = ctk.CTkOptionMenu(
                self.datos_frame,
                values=self.obtener_unidades_por_variable(clave),
                font=("Comfortaa", 12),
                dropdown_font=("Comfortaa", 12),
                width=90
            )
            combo_unidad.grid(row=i, column=2, padx=14, pady=5, sticky="ew")
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

        else:
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
                resultado_base, unidad_base, procedimiento = calcular_mru(objetivo, datos)
            elif movimiento == "MRUV":
                resultado_base, unidad_base, procedimiento = calcular_mruv(objetivo, datos)
            elif movimiento == "CAÍDA LIBRE":
                resultado_base, unidad_base, procedimiento = calcular_caida_libre(objetivo, datos)
            else:
                resultado_base, unidad_base, procedimiento = calcular_lanzamiento_vertical(objetivo, datos)

            unidad_salida = self.unit_boxes[objetivo].get()
            resultado_convertido = self.convertir_desde_base(objetivo, resultado_base, unidad_salida)

            self.ultimo_calculo = {
                "movimiento": movimiento,
                "objetivo": objetivo,
                "objetivo_amigable": objetivo_amigable,
                "datos": datos,
                "resultado_base": resultado_base,
                "unidad_base": unidad_base,
                "unidad_salida": unidad_salida,
                "resultado_convertido": resultado_convertido
            }

            texto_resultado = (
                f"Movimiento seleccionado: {movimiento}\n"
                f"Dato calculado: {objetivo_amigable}\n\n"
                "Datos ingresados:\n"
                f"{self.formatear_datos_ingresados()}\n\n"
                f"{procedimiento}\n\n"
                f"Resultado final: {resultado_convertido:.2f} {unidad_salida}"
            )

            self.mostrar_resultado(texto_resultado)
            self.agregar_al_historial(texto_resultado)

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

        self.ultimo_calculo = None
        self.actualizar_estado_entradas()
        self.mostrar_resultado("Aquí aparecerá el resultado del cálculo.")

    def agregar_al_historial(self, texto):
        self.historial.append(texto)

        self.historial_text.configure(state="normal")
        self.historial_text.insert("end", texto + "\n\n")
        self.historial_text.configure(state="disabled")
        self.historial_text.see("end")

    def limpiar_historial(self):
        self.historial.clear()

        self.historial_text.configure(state="normal")
        self.historial_text.delete("1.0", "end")
        self.historial_text.configure(state="disabled")

    def crear_intervalo_tiempo(self, tiempo_final, pasos=80):
        return [(tiempo_final * i) / (pasos - 1) for i in range(pasos)]

    def generar_grafico(self):
        if self.ultimo_calculo is None:
            messagebox.showwarning(
                "Sin cálculo",
                "Primero debe realizar un cálculo antes de generar una gráfica."
            )
            return

        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        movimiento = self.ultimo_calculo["movimiento"]
        objetivo = self.ultimo_calculo["objetivo"]
        datos = self.ultimo_calculo["datos"]
        resultado = self.ultimo_calculo["resultado_base"]

        try:
            tiempos, valores, titulo, eje_y = self.obtener_datos_grafico(
                movimiento,
                objetivo,
                datos,
                resultado
            )

            fig = Figure(figsize=(8, 4.5), dpi=100)
            fig.tight_layout()
            ax = fig.add_subplot(111)

            ax.plot(tiempos, valores)
            ax.set_title(titulo)
            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel(eje_y)
            ax.grid(True)
            ax.set_facecolor("#f8f9fa")

            self.canvas_grafico = FigureCanvasTkAgg(fig, master=self.grafico_frame)
            self.canvas_grafico.draw()
            self.canvas_grafico.get_tk_widget().pack(fill="both", expand=True)

            self.tabs.set("Gráfica")

        except Exception as e:
            messagebox.showerror("Error al graficar", str(e))

    def obtener_datos_grafico(self, movimiento, objetivo, datos, resultado):
        g = 9.8

        if movimiento == "MRU":
            if objetivo == "distancia":
                velocidad = datos["velocidad"]
                tiempo_final = datos["tiempo"]
            elif objetivo == "velocidad":
                velocidad = resultado
                tiempo_final = datos["tiempo"]
            else:
                velocidad = datos["velocidad"]
                tiempo_final = resultado

            if tiempo_final <= 0:
                raise ValueError("El tiempo debe ser mayor que 0 para generar la gráfica.")

            tiempos = self.crear_intervalo_tiempo(tiempo_final)
            valores = [velocidad * t for t in tiempos]
            return tiempos, valores, "MRU: Distancia vs Tiempo", "Distancia (m)"

        elif movimiento == "MRUV":
            velocidad_inicial = datos["velocidad_inicial"]

            if objetivo == "aceleracion":
                aceleracion = resultado
                tiempo_final = datos["tiempo"]
            else:
                aceleracion = datos["aceleracion"]
                tiempo_final = datos["tiempo"]

            if tiempo_final <= 0:
                raise ValueError("El tiempo debe ser mayor que 0 para generar la gráfica.")

            tiempos = self.crear_intervalo_tiempo(tiempo_final)
            valores = [
                (velocidad_inicial * t) + (0.5 * aceleracion * (t ** 2))
                for t in tiempos
            ]
            return tiempos, valores, "MRUV: Distancia vs Tiempo", "Distancia (m)"

        elif movimiento == "CAÍDA LIBRE":
            if objetivo == "tiempo":
                tiempo_final = resultado
            else:
                tiempo_final = datos["tiempo"]

            if tiempo_final <= 0:
                raise ValueError("El tiempo debe ser mayor que 0 para generar la gráfica.")

            tiempos = self.crear_intervalo_tiempo(tiempo_final)
            valores = [0.5 * g * (t ** 2) for t in tiempos]
            return tiempos, valores, "Caída Libre: Altura vs Tiempo", "Altura (m)"

        else:
            velocidad_inicial = datos["velocidad_inicial"]

            if objetivo == "tiempo":
                tiempo_final = resultado
            else:
                tiempo_final = datos["tiempo"]

            if tiempo_final <= 0:
                raise ValueError("El tiempo debe ser mayor que 0 para generar la gráfica.")

            tiempos = self.crear_intervalo_tiempo(tiempo_final)
            valores = [
                (velocidad_inicial * t) - (0.5 * g * (t ** 2))
                for t in tiempos
            ]
            return tiempos, valores, "Lanzamiento Vertical: Altura vs Tiempo", "Altura (m)"
    
    def obtener_fecha_actual(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    def exportar_resultado_txt(self):
        contenido = self.resultado_text.get("1.0", "end").strip()
    
        if not contenido or contenido == "Aquí aparecerá el resultado del cálculo.":
            messagebox.showwarning(
                "Sin resultado",
                "Primero debe realizar un cálculo antes de exportar el resultado."
            )
            return
    
        nombre_sugerido = f"resultado_calculo_{self.obtener_fecha_actual()}.txt"
    
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=nombre_sugerido,
            filetypes=[
                ("Archivo de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )
    
        if not ruta_archivo:
            return
    
        try:
            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                archivo.write("Calculadora de Física - Cinemática\n")
                archivo.write("Resultado exportado\n")
                archivo.write("====================================\n\n")
                archivo.write(contenido)
    
            messagebox.showinfo(
                "Exportación exitosa",
                "El resultado fue exportado correctamente."
            )
    
        except Exception as e:
            messagebox.showerror(
                "Error al exportar",
                f"No se pudo exportar el resultado:\n{e}"
            )
    
    
    def exportar_historial_txt(self):
        if not self.historial:
            messagebox.showwarning(
                "Historial vacío",
                "No hay cálculos en el historial para exportar."
            )
            return
    
        nombre_sugerido = f"historial_calculos_{self.obtener_fecha_actual()}.txt"
    
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=nombre_sugerido,
            filetypes=[
                ("Archivo de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )
    
        if not ruta_archivo:
            return
    
        try:
            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                archivo.write("Calculadora de Física - Cinemática\n")
                archivo.write("Historial de cálculos\n")
                archivo.write("====================================\n\n")
    
                for index, calculo in enumerate(self.historial, start=1):
                    archivo.write(f"Cálculo #{index}\n")
                    archivo.write("------------------------------------\n")
                    archivo.write(calculo)
                    archivo.write("\n\n")
    
            messagebox.showinfo(
                "Exportación exitosa",
                "El historial fue exportado correctamente."
            )
    
        except Exception as e:
            messagebox.showerror(
                "Error al exportar",
                f"No se pudo exportar el historial:\n{e}"
            )
    
    def cambiar_tema(self, tema):
        if tema == "Claro":
            ctk.set_appearance_mode("light")
            self.aplicar_colores_tema_claro()
        else:
            ctk.set_appearance_mode("dark")
            self.aplicar_colores_tema_oscuro()
    
    def aplicar_colores_tema_claro(self):
        self.header.configure(fg_color = "#d9e9f7")
        self.title_label.configure(text_color = "#16324f")
        self.subtitle_label.configure(text_color = "#35516b")
        self.tema_label.configure(text_color = "#35516b")
    
    def aplicar_colores_tema_oscuro(self):
        self.header.configure(fg_color = "#1f2d3a")
        self.title_label.configure(text_color = "#eaf2f8")
        self.subtitle_label.configure(text_color = "#d6eaf8")
        self.tema_label.configure(text_color = "#d6eaf8")


if __name__ == "__main__":
    root = ctk.CTk()
    app = CalculadoraFisicaApp(root)
    root.mainloop()
    
#K247