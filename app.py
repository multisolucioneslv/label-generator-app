import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Formulario etiquetas")
        self.geometry("1200x800")
        self.resizable(False, False)

        self.create_header()
        self.create_main_content()

    def create_header(self):
        header_frame = tk.Frame(self, bg="#33dcb8", height=60)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        button_style = {
            "bg": "#34495e",
            "fg": "white",
            "font": ("Arial", 12),
            "relief": "flat",
            "padx": 20,
            "pady": 10,
            "cursor": "hand2"
        }

        home_btn = tk.Button(header_frame, text="Inicio", **button_style, command=self.show_home)
        home_btn.pack(side="left", padx=10, pady=10)

        config_btn = tk.Button(header_frame, text="Configuraciones", **button_style, command=self.show_config)
        config_btn.pack(side="left", padx=10, pady=10)

        admin_btn = tk.Button(header_frame, text="Administración", **button_style, command=self.show_admin)
        admin_btn.pack(side="left", padx=10, pady=10)

    def create_main_content(self):
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        self.label = tk.Label(self.main_frame, text="Hola Mundo", font=("Arial", 24))
        self.label.place(relx=0.5, rely=0.5, anchor="center")

    def show_home(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Crear canvas con scrollbar para responsividad
        canvas = tk.Canvas(self.main_frame, bg="#f0f4f8")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f4f8")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Header con título principal (simulando gradiente con degradado)
        header_section = tk.Frame(scrollable_frame, bg="#667eea")
        header_section.pack(fill="x", pady=(0, 30))

        # Crear efecto de gradiente con múltiples frames
        gradient_frame1 = tk.Frame(header_section, bg="#667eea", height=20)
        gradient_frame1.pack(fill="x")
        gradient_frame2 = tk.Frame(header_section, bg="#6b7ce8", height=20)
        gradient_frame2.pack(fill="x")
        gradient_frame3 = tk.Frame(header_section, bg="#7078e6", height=20)
        gradient_frame3.pack(fill="x")

        main_title = tk.Label(header_section, text="📋 Generador de Etiquetas de Envío",
                             font=("Segoe UI", 28, "bold"), bg="#667eea", fg="white")
        main_title.pack(pady=(10, 15))

        subtitle = tk.Label(header_section, text="Complete la información del remitente y destinatario",
                           font=("Segoe UI", 12), bg="#667eea", fg="#e8f0ff")
        subtitle.pack(pady=(0, 20))

        # Container principal para los formularios
        forms_container = tk.Frame(scrollable_frame, bg="#f0f4f8")
        forms_container.pack(fill="both", expand=True, padx=40, pady=20)

        # Formulario Remitente (lado izquierdo)
        remitente_frame = tk.Frame(forms_container, bg="white", relief="flat", bd=0)
        remitente_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Añadir sombra visual
        self.add_shadow_effect(remitente_frame)

        # Header del formulario remitente
        remitente_header = tk.Frame(remitente_frame, bg="#4CAF50", height=60)
        remitente_header.pack(fill="x")
        remitente_header.pack_propagate(False)

        remitente_icon = tk.Label(remitente_header, text="📤", font=("Segoe UI", 20), bg="#4CAF50")
        remitente_icon.pack(side="left", padx=20, pady=15)

        remitente_title = tk.Label(remitente_header, text="Datos del Remitente",
                                 font=("Segoe UI", 16, "bold"), bg="#4CAF50", fg="white")
        remitente_title.pack(side="left", pady=15)

        # Campos del formulario remitente
        self.create_modern_form_fields(remitente_frame, "remitente", "#4CAF50")

        # Formulario Destinatario (lado derecho)
        destinatario_frame = tk.Frame(forms_container, bg="white", relief="flat", bd=0)
        destinatario_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))

        # Añadir sombra visual
        self.add_shadow_effect(destinatario_frame)

        # Header del formulario destinatario
        destinatario_header = tk.Frame(destinatario_frame, bg="#2196F3", height=60)
        destinatario_header.pack(fill="x")
        destinatario_header.pack_propagate(False)

        destinatario_icon = tk.Label(destinatario_header, text="📥", font=("Segoe UI", 20), bg="#2196F3")
        destinatario_icon.pack(side="left", padx=20, pady=15)

        destinatario_title = tk.Label(destinatario_header, text="Datos del Destinatario",
                                    font=("Segoe UI", 16, "bold"), bg="#2196F3", fg="white")
        destinatario_title.pack(side="left", pady=15)

        # Campos del formulario destinatario
        self.create_modern_form_fields(destinatario_frame, "destinatario", "#2196F3")

        # Botón de acción principal
        action_frame = tk.Frame(scrollable_frame, bg="#f0f4f8")
        action_frame.pack(fill="x", pady=30)

        generate_btn = tk.Button(action_frame, text="🏷️ Generar Etiqueta",
                               font=("Segoe UI", 14, "bold"), bg="#FF6B35", fg="white",
                               relief="flat", padx=40, pady=15, cursor="hand2",
                               command=self.generate_label)
        generate_btn.pack()

        # Configurar el canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel para scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def add_shadow_effect(self, widget):
        # Simular sombra con bordes
        shadow_frame = tk.Frame(widget.master, bg="#e0e0e0", height=widget.winfo_reqheight()+4, width=widget.winfo_reqwidth()+4)
        shadow_frame.place(x=widget.winfo_x()+2, y=widget.winfo_y()+2)
        widget.lift()

    def create_modern_form_fields(self, parent_frame, form_type, accent_color):
        # Contenedor para los campos con padding moderno
        fields_frame = tk.Frame(parent_frame, bg="white")
        fields_frame.pack(padx=30, pady=20, fill="both", expand=True)

        # Estilo para campos de entrada
        entry_style = {
            "font": ("Segoe UI", 11),
            "relief": "flat",
            "bd": 0,
            "highlightthickness": 2,
            "highlightcolor": accent_color,
            "highlightbackground": "#e0e0e0",
            "bg": "#f8f9fa",
            "fg": "#2c3e50"
        }

        # Campo Nombre con animación
        nombre_container = tk.Frame(fields_frame, bg="white")
        nombre_container.pack(fill="x", pady=(0, 20))

        nombre_label = tk.Label(nombre_container, text="👤 Nombre completo",
                               bg="white", fg="#5f6368", font=("Segoe UI", 10, "bold"))
        nombre_label.pack(anchor="w", pady=(0, 5))

        nombre_entry = tk.Entry(nombre_container, **entry_style)
        self.add_placeholder_animation(nombre_entry, "Ingrese el nombre completo")
        nombre_entry.pack(fill="x", ipady=12)

        # Campo Dirección
        direccion_container = tk.Frame(fields_frame, bg="white")
        direccion_container.pack(fill="x", pady=(0, 20))

        direccion_label = tk.Label(direccion_container, text="🏠 Dirección",
                                  bg="white", fg="#5f6368", font=("Segoe UI", 10, "bold"))
        direccion_label.pack(anchor="w", pady=(0, 5))

        direccion_entry = tk.Entry(direccion_container, **entry_style)
        self.add_placeholder_animation(direccion_entry, "Calle, número, colonia...")
        direccion_entry.pack(fill="x", ipady=12)

        # Frame para Ciudad, Estado, ZIP con diseño en grid
        location_label = tk.Label(fields_frame, text="📍 Ubicación",
                                bg="white", fg="#5f6368", font=("Segoe UI", 10, "bold"))
        location_label.pack(anchor="w", pady=(0, 5))

        location_frame = tk.Frame(fields_frame, bg="white")
        location_frame.pack(fill="x", pady=(0, 10))

        # Campo Ciudad
        ciudad_frame = tk.Frame(location_frame, bg="white")
        ciudad_frame.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ciudad_label = tk.Label(ciudad_frame, text="Ciudad", bg="white", fg="#8e8e8e", font=("Segoe UI", 9))
        ciudad_label.pack(anchor="w")
        ciudad_entry = tk.Entry(ciudad_frame, **entry_style)
        self.add_placeholder_animation(ciudad_entry, "Ciudad")
        ciudad_entry.pack(fill="x", ipady=10)

        # Campo Estado
        estado_frame = tk.Frame(location_frame, bg="white")
        estado_frame.pack(side="left", fill="x", expand=True, padx=(4, 4))
        estado_label = tk.Label(estado_frame, text="Estado", bg="white", fg="#8e8e8e", font=("Segoe UI", 9))
        estado_label.pack(anchor="w")
        estado_entry = tk.Entry(estado_frame, **entry_style)
        self.add_placeholder_animation(estado_entry, "Estado")
        estado_entry.pack(fill="x", ipady=10)

        # Campo ZIP
        zip_frame = tk.Frame(location_frame, bg="white")
        zip_frame.pack(side="left", fill="x", expand=True, padx=(8, 0))
        zip_label = tk.Label(zip_frame, text="Código Postal", bg="white", fg="#8e8e8e", font=("Segoe UI", 9))
        zip_label.pack(anchor="w")
        zip_entry = tk.Entry(zip_frame, **entry_style)
        self.add_placeholder_animation(zip_entry, "00000")
        zip_entry.pack(fill="x", ipady=10)

        # Barra de progreso visual
        progress_frame = tk.Frame(fields_frame, bg="white")
        progress_frame.pack(fill="x", pady=(20, 0))

        progress_label = tk.Label(progress_frame, text="📊 Progreso del formulario",
                                bg="white", fg="#5f6368", font=("Segoe UI", 9))
        progress_label.pack(anchor="w", pady=(0, 5))

        progress_bar = ttk.Progressbar(progress_frame, length=300, mode='determinate')
        progress_bar.pack(fill="x")
        progress_bar['value'] = 0

        # Guardar referencias de los campos para cada formulario
        if not hasattr(self, 'form_fields'):
            self.form_fields = {}

        self.form_fields[form_type] = {
            'nombre': nombre_entry,
            'direccion': direccion_entry,
            'ciudad': ciudad_entry,
            'estado': estado_entry,
            'zip': zip_entry,
            'progress': progress_bar
        }

        # Vincular eventos para actualizar progreso
        for field in [nombre_entry, direccion_entry, ciudad_entry, estado_entry, zip_entry]:
            field.bind('<KeyRelease>', lambda e, t=form_type: self.update_progress(t))
            field.bind('<FocusOut>', lambda e, t=form_type: self.update_progress(t))

    def add_placeholder_animation(self, entry, placeholder_text):
        entry.placeholder_text = placeholder_text
        entry.placeholder_active = True

        def on_focus_in(event):
            if entry.placeholder_active:
                entry.delete(0, tk.END)
                entry.config(fg='#2c3e50')
                entry.placeholder_active = False

        def on_focus_out(event):
            if not entry.get():
                entry.placeholder_active = True
                entry.insert(0, placeholder_text)
                entry.config(fg='#a0a0a0')

        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

        # Configurar placeholder inicial
        entry.insert(0, placeholder_text)
        entry.config(fg='#a0a0a0')

    def update_progress(self, form_type):
        if hasattr(self, 'form_fields') and form_type in self.form_fields:
            fields = self.form_fields[form_type]
            filled_fields = 0
            total_fields = 5

            for field_name, field_widget in fields.items():
                if field_name != 'progress' and field_widget.get() and not field_widget.placeholder_active:
                    filled_fields += 1

            progress_percentage = (filled_fields / total_fields) * 100
            fields['progress']['value'] = progress_percentage

    def generate_label(self):
        # Placeholder para funcionalidad de generación de etiqueta
        print("Generando etiqueta...")

        if hasattr(self, 'form_fields'):
            remitente_data = {}
            destinatario_data = {}

            if 'remitente' in self.form_fields:
                for field, widget in self.form_fields['remitente'].items():
                    if field != 'progress':
                        remitente_data[field] = widget.get() if not widget.placeholder_active else ""

            if 'destinatario' in self.form_fields:
                for field, widget in self.form_fields['destinatario'].items():
                    if field != 'progress':
                        destinatario_data[field] = widget.get() if not widget.placeholder_active else ""

            print(f"Datos remitente: {remitente_data}")
            print(f"Datos destinatario: {destinatario_data}")

    def show_config(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        config_label = tk.Label(self.main_frame, text="Configuraciones", font=("Arial", 20))
        config_label.place(relx=0.5, rely=0.5, anchor="center")

    def show_admin(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        admin_label = tk.Label(self.main_frame, text="Administración", font=("Arial", 20))
        admin_label.place(relx=0.5, rely=0.5, anchor="center")

if __name__ == "__main__":
    app = App()
    app.mainloop()
