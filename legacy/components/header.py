import tkinter as tk
from config.settings import COLORS, FONTS, SPACING

class HeaderComponent:
    def __init__(self, parent, callbacks):
        self.parent = parent
        self.callbacks = callbacks
        self.buttons = {}
        self.create_header()

    def create_header(self):
        header_frame = tk.Frame(self.parent, bg=COLORS['primary'], height=SPACING['header_height'])
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        # Estilos para botones
        self.button_style_normal = {
            "bg": "#34495e",
            "fg": "white",
            "font": FONTS['subtitle'],
            "relief": "flat",
            "padx": 20,
            "pady": 10,
            "cursor": "hand2"
        }

        self.button_style_active = {
            "bg": "#2c3e50",
            "fg": "#33dcb8",
            "font": ('Segoe UI', 12, 'bold'),
            "relief": "flat",
            "padx": 20,
            "pady": 10,
            "cursor": "hand2"
        }

        # Crear botones con referencias guardadas
        self.buttons['home'] = tk.Button(header_frame, text="🏠 Inicio", **self.button_style_active,
                                       command=self.callbacks['show_home'])
        self.buttons['home'].pack(side="left", padx=10, pady=10)

        self.buttons['config'] = tk.Button(header_frame, text="⚙️ Configuraciones", **self.button_style_normal,
                                         command=self.callbacks['show_config'])
        self.buttons['config'].pack(side="left", padx=10, pady=10)

        self.buttons['admin'] = tk.Button(header_frame, text="👨‍💼 Administración", **self.button_style_normal,
                                        command=self.callbacks['show_admin'])
        self.buttons['admin'].pack(side="left", padx=10, pady=10)

    def update_active_button(self, active_view):
        """Actualiza el estilo del botón activo"""
        for view_name, button in self.buttons.items():
            if view_name == active_view:
                button.config(**self.button_style_active)
            else:
                button.config(**self.button_style_normal)