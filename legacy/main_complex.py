import tkinter as tk
from config.settings import WINDOW_CONFIG
from components.header import HeaderComponent
from ui.home_view import HomeView
from ui.config_view import ConfigView
from ui.admin_view import AdminView

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(WINDOW_CONFIG['title'])
        self.geometry(f"{WINDOW_CONFIG['width']}x{WINDOW_CONFIG['height']}")
        self.resizable(WINDOW_CONFIG['resizable'], WINDOW_CONFIG['resizable'])

        # Configurar tamaño mínimo
        self.minsize(WINDOW_CONFIG['min_width'], WINDOW_CONFIG['min_height'])

        # Centrar ventana en la pantalla
        self.center_window()

        # Variable para rastrear vista activa
        self.current_view = "home"

        # Inicializar vistas
        self.home_view = None
        self.config_view = None
        self.admin_view = None

        self.setup_ui()

        # GARANTIZAR que siempre inicie en Home
        self.after(100, self.force_home_view)

    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (WINDOW_CONFIG['width'] // 2)
        y = (self.winfo_screenheight() // 2) - (WINDOW_CONFIG['height'] // 2)
        self.geometry(f"{WINDOW_CONFIG['width']}x{WINDOW_CONFIG['height']}+{x}+{y}")

    def setup_ui(self):
        # Crear header con callbacks
        header_callbacks = {
            'show_home': self.show_home,
            'show_config': self.show_config,
            'show_admin': self.show_admin
        }

        self.header = HeaderComponent(self, header_callbacks)

        # Crear frame principal para contenido
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        # Mostrar vista inicial
        self.show_home()

    def show_home(self):
        self.current_view = "home"
        if not self.home_view:
            self.home_view = HomeView(self.main_frame)
        self.home_view.create_home_view()
        self.update_header_buttons()

    def show_config(self):
        self.current_view = "config"
        if not self.config_view:
            self.config_view = ConfigView(self.main_frame)
        self.config_view.create_config_view()
        self.update_header_buttons()

    def show_admin(self):
        self.current_view = "admin"
        if not self.admin_view:
            self.admin_view = AdminView(self.main_frame)
        self.admin_view.create_admin_view()
        self.update_header_buttons()

    def force_home_view(self):
        """Fuerza la vista a Home si no está ya activa"""
        if self.current_view != "home":
            self.show_home()

    def update_header_buttons(self):
        """Actualiza el estilo de los botones del header para mostrar el activo"""
        if hasattr(self.header, 'update_active_button'):
            self.header.update_active_button(self.current_view)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()