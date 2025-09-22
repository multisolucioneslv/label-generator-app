import tkinter as tk
from tkinter import ttk
from config.settings import COLORS, FONTS, SPACING, WINDOW_CONFIG, BREAKPOINTS
from components.form_fields import FormFieldsComponent

class HomeView:
    def __init__(self, parent):
        self.parent = parent
        self.form_component = FormFieldsComponent()

    def create_home_view(self):
        # Limpiar contenido previo
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Determinar si usar layout responsive
        window_width = WINDOW_CONFIG['width']
        use_vertical_layout = window_width < BREAKPOINTS['medium'] or SPACING.get('vertical_layout', False)

        # Container principal con scroll si es necesario
        if use_vertical_layout or window_width < BREAKPOINTS['large']:
            main_container = self._create_scrollable_container()
        else:
            main_container = tk.Frame(self.parent, bg=COLORS['background'])
            main_container.pack(fill="both", expand=True)

        # Header compacto
        self._create_compact_header(main_container)

        # Container para formularios - responsive
        forms_container = tk.Frame(main_container, bg=COLORS['background'])
        forms_container.pack(fill="both", expand=True, padx=SPACING['section_spacing'], pady=15)

        if use_vertical_layout:
            # Layout vertical para pantallas pequeñas
            self._create_vertical_layout(forms_container)
        else:
            # Layout horizontal para pantallas grandes
            self._create_horizontal_layout(forms_container)

        # Botón de acción centrado
        self._create_action_button(main_container)

    def _create_scrollable_container(self):
        """Crea un container con scroll para pantallas pequeñas"""
        canvas = tk.Canvas(self.parent, bg=COLORS['background'])
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['background'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        return scrollable_frame

    def _create_horizontal_layout(self, parent):
        """Layout horizontal para pantallas grandes"""
        # Formulario Remitente (izquierda)
        remitente_frame = self._create_form_card(parent, "📤 Datos del Remitente",
                                                COLORS['remitente'], "left")
        self.form_component.create_modern_form_fields(remitente_frame, "remitente", COLORS['remitente'])

        # Formulario Destinatario (derecha)
        destinatario_frame = self._create_form_card(parent, "📥 Datos del Destinatario",
                                                   COLORS['destinatario'], "right")
        self.form_component.create_modern_form_fields(destinatario_frame, "destinatario", COLORS['destinatario'])

    def _create_vertical_layout(self, parent):
        """Layout vertical para pantallas pequeñas"""
        # Formulario Remitente (arriba)
        remitente_frame = self._create_form_card(parent, "📤 Datos del Remitente",
                                                COLORS['remitente'], "top")
        self.form_component.create_modern_form_fields(remitente_frame, "remitente", COLORS['remitente'])

        # Espaciado entre formularios
        tk.Frame(parent, bg=COLORS['background'], height=SPACING['form_gap']).pack(fill="x")

        # Formulario Destinatario (abajo)
        destinatario_frame = self._create_form_card(parent, "📥 Datos del Destinatario",
                                                   COLORS['destinatario'], "bottom")
        self.form_component.create_modern_form_fields(destinatario_frame, "destinatario", COLORS['destinatario'])

    def _create_compact_header(self, parent):
        header_section = tk.Frame(parent, bg=COLORS['secondary'], height=80)
        header_section.pack(fill="x")
        header_section.pack_propagate(False)

        title_frame = tk.Frame(header_section, bg=COLORS['secondary'])
        title_frame.pack(expand=True, fill="both")

        main_title = tk.Label(title_frame, text="📋 Generador de Etiquetas",
                             font=('Segoe UI', 20, 'bold'), bg=COLORS['secondary'], fg="white")
        main_title.pack(pady=(15, 5))

        subtitle = tk.Label(title_frame, text="Complete la información para generar su etiqueta de envío",
                           font=FONTS['subtitle'], bg=COLORS['secondary'], fg="#e8f0ff")
        subtitle.pack()

    def _create_form_card(self, parent, title, color, position):
        # Frame principal del formulario
        form_frame = tk.Frame(parent, bg=COLORS['white'], relief="solid", bd=1)

        # Posicionamiento responsive
        if position == "left":
            form_frame.pack(side="left", fill="both", expand=True, padx=(0, SPACING['form_gap']))
        elif position == "right":
            form_frame.pack(side="right", fill="both", expand=True, padx=(SPACING['form_gap'], 0))
        elif position == "top":
            form_frame.pack(fill="x", pady=(0, SPACING['form_gap']))
        elif position == "bottom":
            form_frame.pack(fill="x", pady=(SPACING['form_gap'], 0))

        # Header del formulario con altura adaptativa
        header_height = 45 if WINDOW_CONFIG['width'] >= BREAKPOINTS['large'] else 40
        header_frame = tk.Frame(form_frame, bg=color, height=header_height)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        # Título con tamaño de fuente adaptativo
        font_size = 14 if WINDOW_CONFIG['width'] >= BREAKPOINTS['large'] else 12
        title_label = tk.Label(header_frame, text=title,
                              font=('Segoe UI', font_size, 'bold'), bg=color, fg="white")
        title_label.pack(pady=(header_height//3))

        return form_frame

    def _create_action_button(self, parent):
        action_frame = tk.Frame(parent, bg=COLORS['background'])
        action_frame.pack(fill="x", pady=(10, 20))

        # Crear estilo personalizado para el botón
        style = ttk.Style()
        style.configure("Action.TButton",
                       font=FONTS['button'],
                       padding=(20, 10))

        generate_btn = tk.Button(action_frame, text="🏷️ Generar Etiqueta de Envío",
                               font=FONTS['button'], bg=COLORS['accent'], fg="white",
                               relief="flat", padx=30, pady=12, cursor="hand2",
                               command=self._generate_label)
        generate_btn.pack()

        # Efecto hover
        def on_enter(e):
            generate_btn.config(bg="#e55a2b")
        def on_leave(e):
            generate_btn.config(bg=COLORS['accent'])

        generate_btn.bind("<Enter>", on_enter)
        generate_btn.bind("<Leave>", on_leave)

    def _generate_label(self):
        print("Generando etiqueta...")

        remitente_data = self.form_component.get_form_data("remitente")
        destinatario_data = self.form_component.get_form_data("destinatario")

        print(f"Remitente: {remitente_data}")
        print(f"Destinatario: {destinatario_data}")

        # Aquí se puede integrar la lógica de generación de etiquetas
        self._show_success_message()

    def _show_success_message(self):
        # Crear ventana de confirmación
        success_window = tk.Toplevel(self.parent)
        success_window.title("Etiqueta Generada")
        success_window.geometry("300x150")
        success_window.resizable(False, False)
        success_window.configure(bg=COLORS['white'])

        # Centrar la ventana
        success_window.transient(self.parent)
        success_window.grab_set()

        # Contenido
        icon_label = tk.Label(success_window, text="✅", font=("Segoe UI", 30),
                             bg=COLORS['white'])
        icon_label.pack(pady=20)

        message_label = tk.Label(success_window, text="¡Etiqueta generada exitosamente!",
                                font=FONTS['subtitle'], bg=COLORS['white'],
                                fg=COLORS['text_primary'])
        message_label.pack()

        ok_button = tk.Button(success_window, text="Aceptar",
                             font=FONTS['subtitle'], bg=COLORS['accent'], fg="white",
                             relief="flat", padx=20, pady=5,
                             command=success_window.destroy)
        ok_button.pack(pady=20)