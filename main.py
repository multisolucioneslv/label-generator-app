import tkinter as tk
from tkinter import ttk, messagebox

class LabelGeneratorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Formulario etiquetas")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        # Centrar ventana
        self.center_window()

        # Variables para autenticación
        self.is_authenticated = False

        # Variables para rastrear vista actual
        self.current_view = "inicio"

        # Diccionario para almacenar widgets de formularios
        self.form_fields = {}

        # Configurar la interfaz
        self.setup_ui()

    def center_window(self):
        """Centrar ventana en la pantalla"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 600  # 1200/2
        y = (self.root.winfo_screenheight() // 2) - 400  # 800/2
        self.root.geometry(f"1200x800+{x}+{y}")

    def setup_ui(self):
        """Configurar la interfaz completa"""
        self.create_header()
        self.create_main_frame()
        self.show_inicio()  # Mostrar inicio por defecto

    def create_header(self):
        """Crear header con navegación"""
        header_frame = tk.Frame(self.root, bg="#33dcb8", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        # Estilos para botones
        self.btn_style_normal = {
            "bg": "#34495e", "fg": "white", "font": ("Segoe UI", 12),
            "relief": "flat", "padx": 20, "pady": 10, "cursor": "hand2"
        }

        self.btn_style_active = {
            "bg": "#2c3e50", "fg": "#33dcb8", "font": ("Segoe UI", 12, "bold"),
            "relief": "flat", "padx": 20, "pady": 10, "cursor": "hand2"
        }

        # Botones de navegación
        self.btn_inicio = tk.Button(header_frame, text="🏠 Inicio", **self.btn_style_active,
                                   command=self.show_inicio)
        self.btn_inicio.pack(side="left", padx=10, pady=10)

        self.btn_config = tk.Button(header_frame, text="⚙️ Configuración", **self.btn_style_normal,
                                   command=self.show_config)
        self.btn_config.pack(side="left", padx=10, pady=10)

        self.btn_admin = tk.Button(header_frame, text="👨‍💼 Administración", **self.btn_style_normal,
                                  command=self.show_admin)
        self.btn_admin.pack(side="left", padx=10, pady=10)

    def create_main_frame(self):
        """Crear frame principal para contenido"""
        self.main_frame = tk.Frame(self.root, bg="#f0f4f8")
        self.main_frame.pack(fill="both", expand=True)

    def update_header_buttons(self, active_view):
        """Actualizar estilo de botones según vista activa"""
        buttons = {
            "inicio": self.btn_inicio,
            "config": self.btn_config,
            "admin": self.btn_admin
        }

        for view, button in buttons.items():
            if view == active_view:
                button.config(**self.btn_style_active)
            else:
                button.config(**self.btn_style_normal)

    def clear_main_frame(self):
        """Limpiar frame principal"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_inicio(self):
        """Mostrar vista de inicio con formularios"""
        self.current_view = "inicio"
        self.update_header_buttons("inicio")
        self.clear_main_frame()

        # Header de página
        page_header = tk.Frame(self.main_frame, bg="#667eea", height=80)
        page_header.pack(fill="x")
        page_header.pack_propagate(False)

        title_label = tk.Label(page_header, text="📋 Generador de Etiquetas de Envío",
                              font=("Segoe UI", 20, "bold"), bg="#667eea", fg="white")
        title_label.pack(pady=25)

        # Container para formularios
        forms_container = tk.Frame(self.main_frame, bg="#f0f4f8")
        forms_container.pack(fill="both", expand=True, padx=40, pady=30)

        # Formulario Remitente (izquierda)
        remitente_frame = tk.Frame(forms_container, bg="white", relief="solid", bd=1)
        remitente_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Header del formulario remitente
        rem_header = tk.Frame(remitente_frame, bg="#4CAF50", height=50)
        rem_header.pack(fill="x")
        rem_header.pack_propagate(False)

        rem_title = tk.Label(rem_header, text="📤 Datos del Remitente",
                            font=("Segoe UI", 14, "bold"), bg="#4CAF50", fg="white")
        rem_title.pack(pady=15)

        # Campos del remitente
        self.create_form_fields(remitente_frame, "remitente", "#4CAF50")

        # Formulario Destinatario (derecha)
        dest_frame = tk.Frame(forms_container, bg="white", relief="solid", bd=1)
        dest_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))

        # Header del formulario destinatario
        dest_header = tk.Frame(dest_frame, bg="#2196F3", height=50)
        dest_header.pack(fill="x")
        dest_header.pack_propagate(False)

        dest_title = tk.Label(dest_header, text="📥 Datos del Destinatario",
                             font=("Segoe UI", 14, "bold"), bg="#2196F3", fg="white")
        dest_title.pack(pady=15)

        # Campos del destinatario
        self.create_form_fields(dest_frame, "destinatario", "#2196F3")

        # Botón generar etiqueta
        btn_frame = tk.Frame(self.main_frame, bg="#f0f4f8")
        btn_frame.pack(fill="x", pady=20)

        generate_btn = tk.Button(btn_frame, text="🏷️ Generar Etiqueta de Envío",
                               font=("Segoe UI", 14, "bold"), bg="#FF6B35", fg="white",
                               relief="flat", padx=40, pady=15, cursor="hand2",
                               command=self.generate_label)
        generate_btn.pack()

    def create_form_fields(self, parent, form_type, accent_color):
        """Crear campos de formulario optimizados para 1200x800"""
        fields_frame = tk.Frame(parent, bg="white")
        fields_frame.pack(padx=25, pady=20, fill="both", expand=True)

        # Estilo para campos
        entry_style = {
            "font": ("Segoe UI", 11), "relief": "solid", "bd": 1,
            "highlightthickness": 2, "highlightcolor": accent_color,
            "highlightbackground": "#e0e0e0", "bg": "white", "fg": "#2c3e50"
        }

        # Campo Nombre
        name_label = tk.Label(fields_frame, text="👤 Nombre completo",
                             bg="white", fg="#5f6368", font=("Segoe UI", 10, "bold"))
        name_label.pack(anchor="w", pady=(0, 5))

        name_entry = tk.Entry(fields_frame, **entry_style)
        self.add_placeholder(name_entry, "Ingrese el nombre completo")
        name_entry.pack(fill="x", ipady=10, pady=(0, 15))

        # Campo Dirección
        addr_label = tk.Label(fields_frame, text="🏠 Dirección",
                             bg="white", fg="#5f6368", font=("Segoe UI", 10, "bold"))
        addr_label.pack(anchor="w", pady=(0, 5))

        addr_entry = tk.Entry(fields_frame, **entry_style)
        self.add_placeholder(addr_entry, "Calle, número, colonia...")
        addr_entry.pack(fill="x", ipady=10, pady=(0, 15))

        # Ubicación
        loc_label = tk.Label(fields_frame, text="📍 Ubicación",
                            bg="white", fg="#5f6368", font=("Segoe UI", 10, "bold"))
        loc_label.pack(anchor="w", pady=(0, 5))

        # Frame para ciudad, estado, zip
        location_frame = tk.Frame(fields_frame, bg="white")
        location_frame.pack(fill="x", pady=(0, 15))

        # Ciudad
        city_frame = tk.Frame(location_frame, bg="white")
        city_frame.pack(side="left", fill="x", expand=True, padx=(0, 8))

        city_label = tk.Label(city_frame, text="Ciudad", bg="white", fg="#8e8e8e", font=("Segoe UI", 9))
        city_label.pack(anchor="w")

        city_entry = tk.Entry(city_frame, **entry_style)
        self.add_placeholder(city_entry, "Ciudad")
        city_entry.pack(fill="x", ipady=8)

        # Estado
        state_frame = tk.Frame(location_frame, bg="white")
        state_frame.pack(side="left", fill="x", expand=True, padx=(4, 4))

        state_label = tk.Label(state_frame, text="Estado", bg="white", fg="#8e8e8e", font=("Segoe UI", 9))
        state_label.pack(anchor="w")

        state_entry = tk.Entry(state_frame, **entry_style)
        self.add_placeholder(state_entry, "Estado")
        state_entry.pack(fill="x", ipady=8)

        # ZIP
        zip_frame = tk.Frame(location_frame, bg="white")
        zip_frame.pack(side="left", fill="x", expand=True, padx=(8, 0))

        zip_label = tk.Label(zip_frame, text="Código Postal", bg="white", fg="#8e8e8e", font=("Segoe UI", 9))
        zip_label.pack(anchor="w")

        zip_entry = tk.Entry(zip_frame, **entry_style)
        self.add_placeholder(zip_entry, "00000")
        zip_entry.pack(fill="x", ipady=8)

        # Guardar referencias
        self.form_fields[form_type] = {
            'nombre': name_entry,
            'direccion': addr_entry,
            'ciudad': city_entry,
            'estado': state_entry,
            'zip': zip_entry
        }

    def add_placeholder(self, entry, placeholder_text):
        """Agregar placeholder animado a un Entry"""
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

    def show_config(self):
        """Mostrar vista de configuración"""
        self.current_view = "config"
        self.update_header_buttons("config")
        self.clear_main_frame()

        config_label = tk.Label(self.main_frame, text="⚙️ Configuración",
                               font=("Segoe UI", 24), bg="#f0f4f8", fg="#2c3e50")
        config_label.pack(expand=True)

        info_label = tk.Label(self.main_frame, text="Esta sección estará disponible próximamente",
                             font=("Segoe UI", 12), bg="#f0f4f8", fg="#7f8c8d")
        info_label.pack()

    def show_admin(self):
        """Mostrar vista de administración con autenticación"""
        if not self.is_authenticated:
            self.show_auth_modal()
        else:
            self.current_view = "admin"
            self.update_header_buttons("admin")
            self.clear_main_frame()

            admin_label = tk.Label(self.main_frame, text="👨‍💼 Panel de Administración",
                                  font=("Segoe UI", 24), bg="#f0f4f8", fg="#2c3e50")
            admin_label.pack(expand=True)

            info_label = tk.Label(self.main_frame, text="Bienvenido al panel de administración",
                                 font=("Segoe UI", 12), bg="#f0f4f8", fg="#7f8c8d")
            info_label.pack()

            logout_btn = tk.Button(self.main_frame, text="Cerrar Sesión",
                                  font=("Segoe UI", 10), bg="#e74c3c", fg="white",
                                  relief="flat", padx=20, pady=5,
                                  command=self.logout)
            logout_btn.pack(pady=10)

    def show_auth_modal(self):
        """Mostrar modal de autenticación"""
        auth_window = tk.Toplevel(self.root)
        auth_window.title("Autenticación")
        auth_window.geometry("350x250")
        auth_window.resizable(False, False)
        auth_window.configure(bg="white")

        # Centrar modal
        auth_window.transient(self.root)
        auth_window.grab_set()

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 175
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 125
        auth_window.geometry(f"350x250+{x}+{y}")

        # Contenido del modal
        title_label = tk.Label(auth_window, text="🔐 Acceso de Administrador",
                              font=("Segoe UI", 16, "bold"), bg="white", fg="#2c3e50")
        title_label.pack(pady=20)

        # Usuario
        user_label = tk.Label(auth_window, text="Usuario:", bg="white", fg="#5f6368")
        user_label.pack(anchor="w", padx=50)

        user_entry = tk.Entry(auth_window, font=("Segoe UI", 11), width=25)
        user_entry.pack(pady=(5, 15))
        user_entry.focus()

        # Contraseña
        pass_label = tk.Label(auth_window, text="Contraseña:", bg="white", fg="#5f6368")
        pass_label.pack(anchor="w", padx=50)

        pass_entry = tk.Entry(auth_window, font=("Segoe UI", 11), width=25, show="*")
        pass_entry.pack(pady=(5, 20))

        # Botones
        btn_frame = tk.Frame(auth_window, bg="white")
        btn_frame.pack()

        def authenticate():
            if user_entry.get() == "admin" and pass_entry.get() == "123":
                self.is_authenticated = True
                auth_window.destroy()
                self.show_admin()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")

        def cancel():
            auth_window.destroy()

        login_btn = tk.Button(btn_frame, text="Ingresar", bg="#27ae60", fg="white",
                             font=("Segoe UI", 10), relief="flat", padx=20, pady=5,
                             command=authenticate)
        login_btn.pack(side="left", padx=10)

        cancel_btn = tk.Button(btn_frame, text="Cancelar", bg="#95a5a6", fg="white",
                              font=("Segoe UI", 10), relief="flat", padx=20, pady=5,
                              command=cancel)
        cancel_btn.pack(side="left", padx=10)

        # Enter para autenticar
        def on_enter(event):
            authenticate()

        user_entry.bind('<Return>', on_enter)
        pass_entry.bind('<Return>', on_enter)

    def logout(self):
        """Cerrar sesión de administrador"""
        self.is_authenticated = False
        self.show_inicio()

    def generate_label(self):
        """Generar etiqueta con los datos de los formularios"""
        try:
            # Obtener datos de formularios
            remitente_data = {}
            destinatario_data = {}

            if "remitente" in self.form_fields:
                for field, widget in self.form_fields["remitente"].items():
                    value = widget.get() if not widget.placeholder_active else ""
                    remitente_data[field] = value

            if "destinatario" in self.form_fields:
                for field, widget in self.form_fields["destinatario"].items():
                    value = widget.get() if not widget.placeholder_active else ""
                    destinatario_data[field] = value

            # Validar que hay datos
            if not any(remitente_data.values()) or not any(destinatario_data.values()):
                messagebox.showwarning("Advertencia", "Por favor complete los campos necesarios")
                return

            # Mostrar confirmación
            messagebox.showinfo("Éxito", "¡Etiqueta generada exitosamente!")

            # Aquí iría la lógica real de generación de etiquetas
            print("Datos Remitente:", remitente_data)
            print("Datos Destinatario:", destinatario_data)

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar etiqueta: {str(e)}")

    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LabelGeneratorApp()
    app.run()