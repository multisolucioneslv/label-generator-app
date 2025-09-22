import tkinter as tk
from config.settings import COLORS, FONTS

class ConfigView:
    def __init__(self, parent):
        self.parent = parent

    def create_config_view(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Container principal
        container = tk.Frame(self.parent, bg=COLORS['background'])
        container.pack(fill="both", expand=True, padx=40, pady=40)

        # Título
        title = tk.Label(container, text="⚙️ Configuraciones",
                        font=FONTS['title'], bg=COLORS['background'],
                        fg=COLORS['text_primary'])
        title.pack(pady=(0, 30))

        # Card de configuraciones
        config_card = tk.Frame(container, bg=COLORS['white'], relief="solid", bd=1)
        config_card.pack(fill="both", expand=True, padx=50, pady=20)

        # Header del card
        header = tk.Frame(config_card, bg=COLORS['secondary'], height=50)
        header.pack(fill="x")
        header.pack_propagate(False)

        header_title = tk.Label(header, text="Configuraciones de la Aplicación",
                               font=FONTS['header'], bg=COLORS['secondary'], fg="white")
        header_title.pack(pady=15)

        # Contenido de configuraciones
        content = tk.Frame(config_card, bg=COLORS['white'])
        content.pack(fill="both", expand=True, padx=30, pady=30)

        # Configuraciones disponibles
        configs = [
            ("📄 Formato de etiquetas", "PDF, PNG, JPEG"),
            ("🖨️ Impresora predeterminada", "No configurada"),
            ("📏 Tamaño de papel", "A4"),
            ("🌐 Idioma", "Español"),
            ("💾 Carpeta de guardado", "Documentos/Etiquetas")
        ]

        for config_name, config_value in configs:
            self._create_config_item(content, config_name, config_value)

    def _create_config_item(self, parent, name, value):
        item_frame = tk.Frame(parent, bg=COLORS['white'])
        item_frame.pack(fill="x", pady=10)

        name_label = tk.Label(item_frame, text=name,
                             font=FONTS['label'], bg=COLORS['white'],
                             fg=COLORS['text_primary'])
        name_label.pack(side="left")

        value_label = tk.Label(item_frame, text=value,
                              font=FONTS['input'], bg=COLORS['white'],
                              fg=COLORS['text_secondary'])
        value_label.pack(side="right")

        # Línea separadora
        separator = tk.Frame(parent, height=1, bg=COLORS['border'])
        separator.pack(fill="x", pady=5)