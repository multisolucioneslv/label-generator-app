import tkinter as tk
from config.settings import COLORS, FONTS

class AdminView:
    def __init__(self, parent):
        self.parent = parent

    def create_admin_view(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Container principal
        container = tk.Frame(self.parent, bg=COLORS['background'])
        container.pack(fill="both", expand=True, padx=40, pady=40)

        # Título
        title = tk.Label(container, text="👨‍💼 Panel de Administración",
                        font=FONTS['title'], bg=COLORS['background'],
                        fg=COLORS['text_primary'])
        title.pack(pady=(0, 30))

        # Grid de opciones administrativas
        grid_frame = tk.Frame(container, bg=COLORS['background'])
        grid_frame.pack(fill="both", expand=True)

        # Estadísticas
        stats_frame = self._create_admin_card(grid_frame, "📊 Estadísticas", 0, 0)
        self._add_stats_content(stats_frame)

        # Usuarios
        users_frame = self._create_admin_card(grid_frame, "👥 Gestión de Usuarios", 0, 1)
        self._add_users_content(users_frame)

        # Logs
        logs_frame = self._create_admin_card(grid_frame, "📋 Logs del Sistema", 1, 0)
        self._add_logs_content(logs_frame)

        # Mantenimiento
        maintenance_frame = self._create_admin_card(grid_frame, "🔧 Mantenimiento", 1, 1)
        self._add_maintenance_content(maintenance_frame)

    def _create_admin_card(self, parent, title, row, col):
        card = tk.Frame(parent, bg=COLORS['white'], relief="solid", bd=1)
        card.grid(row=row, column=col, sticky="nsew", padx=15, pady=15)

        # Configurar grid weights
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)

        # Header
        header = tk.Frame(card, bg=COLORS['accent'], height=40)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_label = tk.Label(header, text=title,
                              font=FONTS['header'], bg=COLORS['accent'], fg="white")
        title_label.pack(pady=10)

        # Content area
        content = tk.Frame(card, bg=COLORS['white'])
        content.pack(fill="both", expand=True, padx=20, pady=20)

        return content

    def _add_stats_content(self, parent):
        stats = [
            ("Etiquetas generadas hoy", "47"),
            ("Total del mes", "1,234"),
            ("Usuarios activos", "12"),
            ("Errores reportados", "3")
        ]

        for stat_name, stat_value in stats:
            stat_frame = tk.Frame(parent, bg=COLORS['white'])
            stat_frame.pack(fill="x", pady=5)

            name_label = tk.Label(stat_frame, text=stat_name,
                                 font=FONTS['small'], bg=COLORS['white'],
                                 fg=COLORS['text_secondary'])
            name_label.pack(side="left")

            value_label = tk.Label(stat_frame, text=stat_value,
                                  font=FONTS['label'], bg=COLORS['white'],
                                  fg=COLORS['text_primary'])
            value_label.pack(side="right")

    def _add_users_content(self, parent):
        users_list = tk.Listbox(parent, height=6, font=FONTS['small'],
                               bg=COLORS['white'], selectbackground=COLORS['secondary'])
        users_list.pack(fill="both", expand=True)

        users = ["admin@empresa.com", "usuario1@empresa.com", "usuario2@empresa.com",
                "operador@empresa.com", "supervisor@empresa.com"]

        for user in users:
            users_list.insert(tk.END, f"👤 {user}")

    def _add_logs_content(self, parent):
        logs_text = tk.Text(parent, height=6, font=("Consolas", 9),
                           bg="#f8f9fa", fg=COLORS['text_primary'],
                           wrap=tk.WORD)
        logs_text.pack(fill="both", expand=True)

        log_entries = [
            "[INFO] Etiqueta generada exitosamente",
            "[WARN] Conexión lenta detectada",
            "[INFO] Usuario admin conectado",
            "[ERROR] Fallo en impresora",
            "[INFO] Sistema iniciado correctamente"
        ]

        for entry in log_entries:
            logs_text.insert(tk.END, f"{entry}\n")

        logs_text.config(state=tk.DISABLED)

    def _add_maintenance_content(self, parent):
        buttons = [
            ("🔄 Reiniciar Sistema", "#e74c3c"),
            ("🧹 Limpiar Cache", "#f39c12"),
            ("💾 Backup DB", "#27ae60"),
            ("📊 Generar Reporte", "#3498db")
        ]

        for button_text, button_color in buttons:
            btn = tk.Button(parent, text=button_text,
                           font=FONTS['small'], bg=button_color, fg="white",
                           relief="flat", pady=5, cursor="hand2")
            btn.pack(fill="x", pady=2)