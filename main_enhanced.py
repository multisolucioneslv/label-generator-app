import tkinter as tk
from tkinter import ttk, messagebox
import googlemaps
import requests
from datetime import datetime
import threading
from database import db_manager, User, Label, AuditLog
from config import config

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
        self.current_user = None

        # Variables para rastrear vista actual
        self.current_view = "inicio"

        # Diccionario para almacenar widgets de formularios
        self.form_fields = {}

        # Google Maps client
        self.gmaps = None
        self.init_google_maps()

        # Database connection
        self.init_database()

        # Configurar la interfaz
        self.setup_ui()

    def init_database(self):
        """Initialize database connection"""
        try:
            if db_manager.connect():
                db_manager.create_admin_user()
        except Exception as e:
            messagebox.showerror("Error de Base de Datos",
                               f"No se pudo conectar a la base de datos:\n{str(e)}\n\nLa aplicación funcionará sin persistencia de datos.")

    def init_google_maps(self):
        """Initialize Google Maps API client"""
        try:
            api_key = config.GOOGLE_API_KEY
            if api_key:
                self.gmaps = googlemaps.Client(key=api_key)
                # Test API with a simple geocoding request to verify it works
                try:
                    # Simple test to verify API works
                    test_result = self.gmaps.geocode("Mexico City", language='es')
                    if test_result:
                        print("Google Maps API initialized successfully")
                        config.GOOGLE_API_ENABLED = True
                    else:
                        print("Google Maps API test failed - no results")
                        self.gmaps = None
                        config.GOOGLE_API_ENABLED = False
                except Exception as api_error:
                    print(f"Google Maps API test failed: {str(api_error)}")
                    self.gmaps = None
                    config.GOOGLE_API_ENABLED = False
            else:
                self.gmaps = None
                config.GOOGLE_API_ENABLED = False
        except Exception as e:
            print(f"Google Maps API initialization failed: {str(e)}")
            self.gmaps = None
            config.GOOGLE_API_ENABLED = False

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


        self.btn_admin = tk.Button(header_frame, text="👨‍💼 Administración", **self.btn_style_normal,
                                  command=self.show_admin)
        self.btn_admin.pack(side="left", padx=10, pady=10)

        self.btn_historial = tk.Button(header_frame, text="📊 Historial", **self.btn_style_normal,
                                      command=self.show_historial)
        self.btn_historial.pack(side="left", padx=10, pady=10)

    def create_main_frame(self):
        """Crear frame principal para contenido"""
        self.main_frame = tk.Frame(self.root, bg="#f0f4f8")
        self.main_frame.pack(fill="both", expand=True)

    def update_header_buttons(self, active_view):
        """Actualizar estilo de botones según vista activa"""
        buttons = {
            "inicio": self.btn_inicio,
            "admin": self.btn_admin,
            "historial": self.btn_historial
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

        # Campo Dirección con autocompletado
        addr_label = tk.Label(fields_frame, text="🏠 Dirección",
                             bg="white", fg="#5f6368", font=("Segoe UI", 10, "bold"))
        addr_label.pack(anchor="w", pady=(0, 5))

        addr_entry = tk.Entry(fields_frame, **entry_style)
        self.add_placeholder(addr_entry, "Calle, número, colonia...")
        self.add_address_autocomplete(addr_entry, form_type)
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

        # Campo de tracking solo para destinatario
        tracking_entry = None
        if form_type == "destinatario":
            track_label = tk.Label(fields_frame, text="📦 Número de Tracking (Opcional)",
                                 bg="white", fg="#5f6368", font=("Segoe UI", 10, "bold"))
            track_label.pack(anchor="w", pady=(0, 5))

            tracking_entry = tk.Entry(fields_frame, **entry_style)
            self.add_placeholder(tracking_entry, "Número de seguimiento")
            tracking_entry.pack(fill="x", ipady=10, pady=(0, 15))

        # Guardar referencias
        self.form_fields[form_type] = {
            'nombre': name_entry,
            'direccion': addr_entry,
            'ciudad': city_entry,
            'estado': state_entry,
            'zip': zip_entry
        }

        if tracking_entry:
            self.form_fields[form_type]['tracking'] = tracking_entry

    def add_address_autocomplete(self, entry, form_type):
        """Add Google Places autocomplete to address field"""
        if not self.gmaps:
            return

        def on_key_release(event):
            if len(entry.get()) > 3 and not entry.placeholder_active:
                threading.Thread(target=self.fetch_suggestions,
                               args=(entry, entry.get()), daemon=True).start()

        entry.bind('<KeyRelease>', on_key_release)

    def fetch_suggestions(self, entry, query):
        """Fetch address suggestions from Google Places API"""
        try:
            if self.gmaps and config.GOOGLE_API_ENABLED:
                # Get selected country
                country_name = db_manager.get_setting('default_country', 'USA')
                country_code = self.get_country_code(country_name)

                # Use geocoding API which is more reliable than places_autocomplete
                try:
                    # First try with geocoding for better compatibility
                    results = self.gmaps.geocode(
                        address=query + f", {country_name}",
                        language='es',
                        region=country_code
                    )

                    if results:
                        suggestions = []
                        for result in results[:5]:  # Limit to 5 suggestions
                            formatted_address = result.get('formatted_address', '')
                            if formatted_address:
                                suggestions.append(formatted_address)

                        if suggestions:
                            print(f"Sugerencias para '{query}':")
                            for i, suggestion in enumerate(suggestions, 1):
                                print(f"  {i}. {suggestion}")

                            # Show suggestions in a simple way for now
                            self.show_address_suggestions(entry, suggestions)

                except Exception as api_error:
                    if "REQUEST_DENIED" in str(api_error):
                        print("Google API Error: Verifica tu API Key y configuración")
                        print("Asegúrate de haber habilitado Geocoding API")
                    elif "OVER_QUERY_LIMIT" in str(api_error):
                        print("Límite de consultas excedido")
                    else:
                        print(f"Error de API: {api_error}")

        except Exception as e:
            print(f"Error general: {str(e)}")

    def show_address_suggestions(self, entry, suggestions):
        """Show address suggestions in a simple dropdown-like manner"""
        try:
            if suggestions and len(suggestions) > 0:
                current_text = entry.get().strip()

                # Don't autocomplete if text is too short or placeholder is active
                if hasattr(entry, 'placeholder_active') and entry.placeholder_active:
                    return
                if len(current_text) < 3:
                    return

                # Find the best suggestion that starts with or contains the current text
                best_suggestion = None
                for suggestion in suggestions:
                    # Clean the suggestion by removing country suffix
                    clean_suggestion = suggestion

                    # Remove various country suffixes
                    country_suffixes = [", USA", ", Mexico", ", Guatemala", ", El Salvador", ", Honduras", ", Bolivia"]
                    for suffix in country_suffixes:
                        if suffix in clean_suggestion:
                            clean_suggestion = clean_suggestion.split(suffix)[0]

                    # Check if this suggestion is relevant to what user typed
                    if (current_text.lower() in clean_suggestion.lower() or
                        clean_suggestion.lower().startswith(current_text.lower())):
                        best_suggestion = clean_suggestion
                        break

                # Only suggest if we found a good match and it's significantly longer
                if (best_suggestion and
                    len(best_suggestion) > len(current_text) + 5 and  # At least 5 chars longer
                    not best_suggestion.lower() == current_text.lower()):

                    # Don't replace if the suggestion is just a country name
                    country_names = ["USA", "United States", "Mexico", "Guatemala", "El Salvador", "Honduras", "Bolivia"]
                    if any(country.lower() in best_suggestion.lower() and len(best_suggestion) < 30 for country in country_names):
                        return

                    # Suggest completion by extending current text
                    entry.delete(0, tk.END)
                    entry.insert(0, best_suggestion)
                    entry.selection_range(len(current_text), tk.END)

        except Exception as e:
            print(f"Error showing suggestions: {e}")

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

    def show_historial(self):
        """Mostrar vista de historial de etiquetas"""
        self.current_view = "historial"
        self.update_header_buttons("historial")
        self.clear_main_frame()

        # Container principal
        historial_container = tk.Frame(self.main_frame, bg="#f0f4f8")
        historial_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title_label = tk.Label(historial_container, text="📊 Historial de Etiquetas",
                              font=("Segoe UI", 24, "bold"), bg="#f0f4f8", fg="#2c3e50")
        title_label.pack(pady=(0, 20))

        # Frame para filtros
        filters_frame = tk.Frame(historial_container, bg="white", relief="solid", bd=1)
        filters_frame.pack(fill="x", pady=(0, 20))

        filters_title = tk.Label(filters_frame, text="🔍 Filtros",
                               font=("Segoe UI", 12, "bold"), bg="white", fg="#5f6368")
        filters_title.pack(pady=10)

        # Frame para estadísticas
        stats_frame = tk.Frame(historial_container, bg="white", relief="solid", bd=1)
        stats_frame.pack(fill="x", pady=(0, 20))

        self._create_stats_section(stats_frame)

        # Frame para tabla de etiquetas
        table_frame = tk.Frame(historial_container, bg="white", relief="solid", bd=1)
        table_frame.pack(fill="both", expand=True)

        self._create_labels_table(table_frame)

    def _create_stats_section(self, parent):
        """Crear sección de estadísticas"""
        stats_title = tk.Label(parent, text="📈 Estadísticas",
                             font=("Segoe UI", 14, "bold"), bg="white", fg="#2c3e50")
        stats_title.pack(pady=10)

        stats_container = tk.Frame(parent, bg="white")
        stats_container.pack(fill="x", padx=20, pady=(0, 20))

        try:
            session = db_manager.get_session()
            if session:
                # Obtener estadísticas
                total_labels = session.query(Label).count()
                today_labels = session.query(Label).filter(
                    Label.created_at >= datetime.now().strftime('%Y-%m-%d')
                ).count()
                with_tracking = session.query(Label).filter(
                    Label.recipient_tracking != ''
                ).count()

                # Crear cards de estadísticas
                stats_data = [
                    ("Total Etiquetas", str(total_labels), "#4CAF50"),
                    ("Hoy", str(today_labels), "#2196F3"),
                    ("Con Tracking", str(with_tracking), "#FF9800"),
                    ("Sin Tracking", str(total_labels - with_tracking), "#9E9E9E")
                ]

                for i, (label, value, color) in enumerate(stats_data):
                    stat_card = tk.Frame(stats_container, bg=color, width=120, height=80)
                    stat_card.pack(side="left", padx=10, fill="y")
                    stat_card.pack_propagate(False)

                    value_label = tk.Label(stat_card, text=value,
                                         font=("Segoe UI", 18, "bold"), bg=color, fg="white")
                    value_label.pack(pady=(15, 5))

                    desc_label = tk.Label(stat_card, text=label,
                                        font=("Segoe UI", 10), bg=color, fg="white")
                    desc_label.pack()

                session.close()

        except Exception as e:
            error_label = tk.Label(stats_container, text=f"Error cargando estadísticas: {str(e)}",
                                 bg="white", fg="red")
            error_label.pack()

    def _create_labels_table(self, parent):
        """Crear tabla de etiquetas"""
        table_title = tk.Label(parent, text="📋 Listado de Etiquetas",
                             font=("Segoe UI", 14, "bold"), bg="white", fg="#2c3e50")
        table_title.pack(pady=10)

        # Frame con scroll para la tabla
        scroll_frame = tk.Frame(parent, bg="white")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Crear Treeview para la tabla
        columns = ("ID", "Fecha", "Remitente", "Destinatario", "Ciudad Origen", "Ciudad Destino", "Tracking", "Estado")
        tree = ttk.Treeview(scroll_frame, columns=columns, show="headings", height=12)

        # Configurar columnas
        tree.heading("ID", text="ID")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Remitente", text="Remitente")
        tree.heading("Destinatario", text="Destinatario")
        tree.heading("Ciudad Origen", text="Ciudad Origen")
        tree.heading("Ciudad Destino", text="Ciudad Destino")
        tree.heading("Tracking", text="Tracking")
        tree.heading("Estado", text="Estado")

        # Configurar anchos de columnas
        tree.column("ID", width=50)
        tree.column("Fecha", width=100)
        tree.column("Remitente", width=150)
        tree.column("Destinatario", width=150)
        tree.column("Ciudad Origen", width=120)
        tree.column("Ciudad Destino", width=120)
        tree.column("Tracking", width=120)
        tree.column("Estado", width=80)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Cargar datos
        try:
            session = db_manager.get_session()
            if session:
                labels = session.query(Label).order_by(Label.created_at.desc()).all()

                for label in labels:
                    # Formatear fecha
                    fecha = label.created_at.strftime("%d/%m/%Y") if label.created_at else "N/A"

                    # Insertar fila
                    tree.insert("", "end", values=(
                        label.id,
                        fecha,
                        label.sender_name,
                        label.recipient_name,
                        label.sender_city,
                        label.recipient_city,
                        label.recipient_tracking if label.recipient_tracking else "Sin tracking",
                        label.status.title()
                    ))

                session.close()

        except Exception as e:
            # Mostrar error en la tabla
            tree.insert("", "end", values=("Error", str(e), "", "", "", "", "", ""))

        # Empaquetar elementos
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botones de acción
        actions_frame = tk.Frame(parent, bg="white")
        actions_frame.pack(fill="x", padx=20, pady=10)

        refresh_btn = tk.Button(actions_frame, text="🔄 Actualizar",
                              bg="#4CAF50", fg="white", relief="flat",
                              font=("Segoe UI", 10), padx=15, pady=5,
                              command=self.show_historial)
        refresh_btn.pack(side="left", padx=5)

        export_btn = tk.Button(actions_frame, text="📊 Exportar",
                             bg="#2196F3", fg="white", relief="flat",
                             font=("Segoe UI", 10), padx=15, pady=5,
                             command=self._export_labels)
        export_btn.pack(side="left", padx=5)

    def _export_labels(self):
        """Exportar etiquetas a CSV"""
        try:
            import csv
            from tkinter import filedialog
            from datetime import datetime

            # Obtener datos
            session = db_manager.get_session()
            if not session:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return

            labels = session.query(Label).order_by(Label.created_at.desc()).all()

            if not labels:
                messagebox.showwarning("Advertencia", "No hay etiquetas para exportar")
                session.close()
                return

            # Seleccionar archivo
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Guardar reporte de etiquetas",
                initialname=f"etiquetas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )

            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)

                    # Header
                    writer.writerow([
                        'ID', 'Fecha', 'Remitente', 'Direccion Remitente', 'Ciudad Remitente',
                        'Destinatario', 'Direccion Destinatario', 'Ciudad Destinatario',
                        'Tracking', 'Estado'
                    ])

                    # Datos
                    for label in labels:
                        writer.writerow([
                            label.id,
                            label.created_at.strftime("%d/%m/%Y %H:%M") if label.created_at else "",
                            label.sender_name,
                            label.sender_address,
                            f"{label.sender_city}, {label.sender_state}",
                            label.recipient_name,
                            label.recipient_address,
                            f"{label.recipient_city}, {label.recipient_state}",
                            label.recipient_tracking or "Sin tracking",
                            label.status
                        ])

                messagebox.showinfo("Éxito", f"Reporte exportado exitosamente a:\n{filename}")

            session.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")


    def show_admin(self):
        """Mostrar vista de administración con autenticación"""
        if not self.is_authenticated:
            self.show_auth_modal()
        else:
            self.current_view = "admin"
            self.update_header_buttons("admin")
            self.clear_main_frame()

            # Container principal
            admin_container = tk.Frame(self.main_frame, bg="#f0f4f8")
            admin_container.pack(fill="both", expand=True, padx=40, pady=30)

            # Título
            admin_label = tk.Label(admin_container, text="👨‍💼 Panel de Administración",
                                  font=("Segoe UI", 24), bg="#f0f4f8", fg="#2c3e50")
            admin_label.pack(pady=(0, 30))

            # Frame para opciones
            options_frame = tk.Frame(admin_container, bg="#f0f4f8")
            options_frame.pack(fill="both", expand=True)

            # Google API Configuration Card
            self.create_google_api_card(options_frame)

            # Country Configuration Card
            self.create_country_config_card(options_frame)

            # User Registration Card
            self.create_user_registration_card(options_frame)

            # Logout button
            logout_btn = tk.Button(admin_container, text="Cerrar Sesión",
                                  font=("Segoe UI", 10), bg="#e74c3c", fg="white",
                                  relief="flat", padx=20, pady=5,
                                  command=self.logout)
            logout_btn.pack(pady=20)

    def create_google_api_card(self, parent):
        """Create Google API configuration card"""
        api_card = tk.Frame(parent, bg="white", relief="solid", bd=1)
        api_card.pack(fill="x", pady=(0, 20))

        # Header
        api_header = tk.Frame(api_card, bg="#4285f4", height=40)
        api_header.pack(fill="x")
        api_header.pack_propagate(False)

        api_title = tk.Label(api_header, text="🗺️ Configuración Google Places API",
                            font=("Segoe UI", 14, "bold"), bg="#4285f4", fg="white")
        api_title.pack(pady=10)

        # Content
        api_content = tk.Frame(api_card, bg="white")
        api_content.pack(fill="x", padx=20, pady=20)

        # API Key field
        key_label = tk.Label(api_content, text="API Key:",
                            bg="white", fg="#5f6368", font=("Segoe UI", 10, "bold"))
        key_label.pack(anchor="w", pady=(0, 5))

        self.api_key_entry = tk.Entry(api_content, font=("Segoe UI", 11), show="*")
        self.api_key_entry.pack(fill="x", ipady=8, pady=(0, 15))

        # Enable checkbox
        self.api_enabled_var = tk.BooleanVar()
        api_check = tk.Checkbutton(api_content, text="Activar autocompletado de direcciones",
                                  variable=self.api_enabled_var, bg="white",
                                  font=("Segoe UI", 10))
        api_check.pack(anchor="w", pady=(0, 15))

        # Save button
        save_api_btn = tk.Button(api_content, text="Guardar Configuración",
                                bg="#4285f4", fg="white", relief="flat",
                                font=("Segoe UI", 10), padx=20, pady=5,
                                command=self.save_api_config)
        save_api_btn.pack()

        # Load current settings
        self.load_api_settings()

    def create_country_config_card(self, parent):
        """Create country configuration card"""
        country_card = tk.Frame(parent, bg="white", relief="solid", bd=1)
        country_card.pack(fill="x", pady=(0, 20))

        # Header
        country_header = tk.Frame(country_card, bg="#17a2b8", height=40)
        country_header.pack(fill="x")
        country_header.pack_propagate(False)

        country_title = tk.Label(country_header, text="🌎 Configuración de País",
                                font=("Segoe UI", 14, "bold"), bg="#17a2b8", fg="white")
        country_title.pack(pady=10)

        # Content
        country_content = tk.Frame(country_card, bg="white")
        country_content.pack(fill="x", padx=20, pady=20)

        # Country selection
        country_label = tk.Label(country_content, text="País predeterminado para direcciones:",
                                bg="white", fg="#5f6368", font=("Segoe UI", 10, "bold"))
        country_label.pack(anchor="w", pady=(0, 5))

        # Country dropdown
        self.country_var = tk.StringVar()
        self.country_options = [
            "USA", "Mexico", "Guatemala", "El Salvador", "Honduras", "Bolivia"
        ]

        country_combo = ttk.Combobox(country_content, textvariable=self.country_var,
                                   values=self.country_options, state="readonly",
                                   font=("Segoe UI", 11))
        country_combo.pack(fill="x", ipady=8, pady=(0, 15))

        # Info label
        info_label = tk.Label(country_content,
                            text="Este país se utilizará para el autocompletado de direcciones.",
                            bg="white", fg="#6c757d", font=("Segoe UI", 9))
        info_label.pack(anchor="w", pady=(0, 15))

        # Save button
        save_country_btn = tk.Button(country_content, text="Guardar País",
                                   bg="#17a2b8", fg="white", relief="flat",
                                   font=("Segoe UI", 10), padx=20, pady=5,
                                   command=self.save_country_config)
        save_country_btn.pack()

        # Load current country
        self.load_country_settings()

    def create_user_registration_card(self, parent):
        """Create user registration card"""
        user_card = tk.Frame(parent, bg="white", relief="solid", bd=1)
        user_card.pack(fill="x", pady=20)

        # Header
        user_header = tk.Frame(user_card, bg="#28a745", height=40)
        user_header.pack(fill="x")
        user_header.pack_propagate(False)

        user_title = tk.Label(user_header, text="👥 Gestión de Usuarios",
                             font=("Segoe UI", 14, "bold"), bg="#28a745", fg="white")
        user_title.pack(pady=10)

        # Content
        user_content = tk.Frame(user_card, bg="white")
        user_content.pack(fill="x", padx=20, pady=20)

        info_text = tk.Label(user_content,
                           text="Registre nuevos usuarios que requerirán aprobación del administrador.",
                           bg="white", fg="#6c757d", font=("Segoe UI", 10))
        info_text.pack(anchor="w", pady=(0, 15))

        # Register new user button
        register_btn = tk.Button(user_content, text="➕ Registrar Nuevo Usuario",
                               bg="#28a745", fg="white", relief="flat",
                               font=("Segoe UI", 12, "bold"), padx=30, pady=10,
                               command=self.show_user_registration_modal)
        register_btn.pack()

    def load_api_settings(self):
        """Load current API settings"""
        try:
            api_key = db_manager.get_setting('google_api_key', '')
            api_enabled = db_manager.get_setting('google_api_enabled', 'false') == 'true'

            if api_key:
                self.api_key_entry.insert(0, api_key)
            self.api_enabled_var.set(api_enabled)
        except:
            pass

    def load_country_settings(self):
        """Load current country settings"""
        try:
            current_country = db_manager.get_setting('default_country', 'USA')
            if current_country in self.country_options:
                self.country_var.set(current_country)
            else:
                self.country_var.set('USA')  # Default to USA
        except:
            self.country_var.set('USA')

    def save_country_config(self):
        """Save country configuration"""
        try:
            selected_country = self.country_var.get()

            if not selected_country:
                messagebox.showwarning("Advertencia", "Selecciona un país.")
                return

            # Save to database
            db_manager.set_setting('default_country', selected_country)

            messagebox.showinfo("Éxito",
                              f"País configurado a {selected_country}.\n"
                              "El autocompletado ahora usará este país.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar país: {str(e)}")

    def get_country_code(self, country_name):
        """Get country code for Google API"""
        country_codes = {
            'USA': 'us',
            'Mexico': 'mx',
            'Guatemala': 'gt',
            'El Salvador': 'sv',
            'Honduras': 'hn',
            'Bolivia': 'bo'
        }
        return country_codes.get(country_name, 'us')

    def save_api_config(self):
        """Save Google API configuration"""
        try:
            api_key = self.api_key_entry.get()
            api_enabled = self.api_enabled_var.get()

            # Save to database
            db_manager.set_setting('google_api_key', api_key)
            db_manager.set_setting('google_api_enabled', str(api_enabled).lower())

            # Update config and reinitialize
            config.GOOGLE_API_KEY = api_key
            config.GOOGLE_API_ENABLED = api_enabled

            # Reinitialize Google Maps
            self.init_google_maps()

            # Test the API immediately
            if self.gmaps and api_enabled:
                try:
                    test_result = self.gmaps.geocode("Ciudad de Mexico", language='es')
                    if test_result:
                        messagebox.showinfo("Éxito",
                                          "Configuración de API guardada correctamente.\n"
                                          "API Key verificada y funcionando.")
                    else:
                        messagebox.showwarning("Advertencia",
                                             "API Key guardada pero no se pudieron obtener resultados de prueba.")
                except Exception as test_error:
                    messagebox.showerror("Error de API",
                                       f"API Key guardada pero falló la prueba:\n{str(test_error)}\n\n"
                                       "Verifica que hayas habilitado Geocoding API en Google Cloud Console.")
            else:
                messagebox.showinfo("Información", "Configuración guardada. API deshabilitada.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar configuración: {str(e)}")

    def show_user_registration_modal(self):
        """Show user registration modal"""
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Registrar Nuevo Usuario")
        reg_window.geometry("400x500")
        reg_window.resizable(False, False)
        reg_window.configure(bg="white")

        # Center modal
        reg_window.transient(self.root)
        reg_window.grab_set()

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 250
        reg_window.geometry(f"400x500+{x}+{y}")

        # Title
        title_label = tk.Label(reg_window, text="👤 Registro de Usuario",
                              font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50")
        title_label.pack(pady=20)

        # Form fields
        fields_frame = tk.Frame(reg_window, bg="white")
        fields_frame.pack(fill="both", expand=True, padx=40)

        # Username
        tk.Label(fields_frame, text="Nombre de usuario:", bg="white", fg="#5f6368").pack(anchor="w", pady=(0, 5))
        username_entry = tk.Entry(fields_frame, font=("Segoe UI", 11))
        username_entry.pack(fill="x", ipady=8, pady=(0, 15))

        # Email
        tk.Label(fields_frame, text="Email:", bg="white", fg="#5f6368").pack(anchor="w", pady=(0, 5))
        email_entry = tk.Entry(fields_frame, font=("Segoe UI", 11))
        email_entry.pack(fill="x", ipady=8, pady=(0, 15))

        # Full name
        tk.Label(fields_frame, text="Nombre completo:", bg="white", fg="#5f6368").pack(anchor="w", pady=(0, 5))
        fullname_entry = tk.Entry(fields_frame, font=("Segoe UI", 11))
        fullname_entry.pack(fill="x", ipady=8, pady=(0, 15))

        # Password
        tk.Label(fields_frame, text="Contraseña:", bg="white", fg="#5f6368").pack(anchor="w", pady=(0, 5))
        password_entry = tk.Entry(fields_frame, font=("Segoe UI", 11), show="*")
        password_entry.pack(fill="x", ipady=8, pady=(0, 15))

        # Confirm password
        tk.Label(fields_frame, text="Confirmar contraseña:", bg="white", fg="#5f6368").pack(anchor="w", pady=(0, 5))
        confirm_entry = tk.Entry(fields_frame, font=("Segoe UI", 11), show="*")
        confirm_entry.pack(fill="x", ipady=8, pady=(0, 20))

        # Buttons
        btn_frame = tk.Frame(reg_window, bg="white")
        btn_frame.pack(pady=20)

        def register_user():
            # Validate fields
            if not all([username_entry.get(), email_entry.get(), fullname_entry.get(),
                       password_entry.get(), confirm_entry.get()]):
                messagebox.showerror("Error", "Todos los campos son requeridos")
                return

            if password_entry.get() != confirm_entry.get():
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return

            try:
                session = db_manager.get_session()
                if not session:
                    messagebox.showerror("Error", "Error de conexión a la base de datos")
                    return

                # Check if username or email exists
                existing = session.query(User).filter(
                    (User.username == username_entry.get()) |
                    (User.email == email_entry.get())
                ).first()

                if existing:
                    messagebox.showerror("Error", "El usuario o email ya existe")
                    session.close()
                    return

                # Create new user
                new_user = User(
                    username=username_entry.get(),
                    email=email_entry.get(),
                    full_name=fullname_entry.get(),
                    is_active=False,  # Requires admin approval
                    is_admin=False
                )
                new_user.set_password(password_entry.get())

                session.add(new_user)
                session.commit()
                session.close()

                messagebox.showinfo("Éxito",
                                   "Usuario registrado correctamente.\nRequiere aprobación del administrador.")
                reg_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar usuario: {str(e)}")

        register_btn = tk.Button(btn_frame, text="Registrar Usuario",
                               bg="#28a745", fg="white", relief="flat",
                               font=("Segoe UI", 11), padx=20, pady=8,
                               command=register_user)
        register_btn.pack(side="left", padx=10)

        cancel_btn = tk.Button(btn_frame, text="Cancelar",
                             bg="#6c757d", fg="white", relief="flat",
                             font=("Segoe UI", 11), padx=20, pady=8,
                             command=reg_window.destroy)
        cancel_btn.pack(side="left", padx=10)

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
            try:
                session = db_manager.get_session()
                if session:
                    user = session.query(User).filter_by(
                        username=user_entry.get(),
                        is_active=True,
                        is_admin=True
                    ).first()

                    if user and user.check_password(pass_entry.get()):
                        self.is_authenticated = True
                        self.current_user = user
                        auth_window.destroy()
                        self.show_admin()
                        session.close()
                        return

                    session.close()

                messagebox.showerror("Error", "Credenciales incorrectas")

            except Exception as e:
                messagebox.showerror("Error", f"Error de autenticación: {str(e)}")

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
        self.current_user = None
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
            required_fields = ['nombre', 'direccion', 'ciudad', 'estado', 'zip']
            sender_valid = all(remitente_data.get(field) for field in required_fields)
            recipient_valid = all(destinatario_data.get(field) for field in required_fields)

            if not sender_valid or not recipient_valid:
                messagebox.showwarning("Advertencia", "Por favor complete todos los campos requeridos")
                return

            # Save to database if connected
            label_id = None
            try:
                session = db_manager.get_session()
                if session:
                    new_label = Label(
                        user_id=self.current_user.id if self.current_user else 1,  # Default to admin
                        sender_name=remitente_data['nombre'],
                        sender_address=remitente_data['direccion'],
                        sender_city=remitente_data['ciudad'],
                        sender_state=remitente_data['estado'],
                        sender_zip=remitente_data['zip'],
                        recipient_name=destinatario_data['nombre'],
                        recipient_address=destinatario_data['direccion'],
                        recipient_city=destinatario_data['ciudad'],
                        recipient_state=destinatario_data['estado'],
                        recipient_zip=destinatario_data['zip'],
                        recipient_tracking=destinatario_data.get('tracking', ''),
                        status='generated'
                    )
                    session.add(new_label)
                    session.commit()
                    label_id = new_label.id
                    session.close()

            except Exception as db_error:
                print(f"Database error: {db_error}")

            # Mostrar confirmación
            success_msg = "¡Etiqueta generada exitosamente!"
            if label_id:
                success_msg += f"\nID de etiqueta: {label_id}"

            messagebox.showinfo("Éxito", success_msg)

            # Log para debug
            print("=== ETIQUETA GENERADA ===")
            print("Datos Remitente:", remitente_data)
            print("Datos Destinatario:", destinatario_data)
            if label_id:
                print(f"Guardada en BD con ID: {label_id}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar etiqueta: {str(e)}")

    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LabelGeneratorApp()
    app.run()