# Configuración de la aplicación
import tkinter as tk

def get_optimal_window_size():
    """Calcula el tamaño óptimo de ventana basado en la resolución de pantalla"""
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana temporal

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    # Calcular dimensiones óptimas (90% de pantalla, con límites)
    optimal_width = min(int(screen_width * 0.9), 1400)  # Máximo 1400px
    optimal_height = min(int(screen_height * 0.85), 900)  # Máximo 900px

    # Garantizar mínimos
    optimal_width = max(optimal_width, 1000)  # Mínimo 1000px
    optimal_height = max(optimal_height, 700)  # Mínimo 700px

    return optimal_width, optimal_height

# Obtener dimensiones dinámicas
DYNAMIC_WIDTH, DYNAMIC_HEIGHT = get_optimal_window_size()

WINDOW_CONFIG = {
    'title': 'Formulario etiquetas',
    'width': DYNAMIC_WIDTH,
    'height': DYNAMIC_HEIGHT,
    'resizable': True,
    'min_width': 1000,
    'min_height': 700
}

# Colores de la aplicación
COLORS = {
    'primary': '#33dcb8',
    'secondary': '#667eea',
    'remitente': '#4CAF50',
    'destinatario': '#2196F3',
    'accent': '#FF6B35',
    'background': '#f0f4f8',
    'white': '#ffffff',
    'text_primary': '#2c3e50',
    'text_secondary': '#5f6368',
    'text_muted': '#8e8e8e',
    'placeholder': '#a0a0a0',
    'border': '#e0e0e0'
}

# Fuentes
FONTS = {
    'title': ('Segoe UI', 28, 'bold'),
    'subtitle': ('Segoe UI', 12),
    'header': ('Segoe UI', 16, 'bold'),
    'label': ('Segoe UI', 10, 'bold'),
    'input': ('Segoe UI', 11),
    'button': ('Segoe UI', 14, 'bold'),
    'small': ('Segoe UI', 9)
}

# Espaciado y dimensiones dinámicas
def get_responsive_spacing():
    """Calcula espaciado basado en el tamaño de ventana"""
    width = DYNAMIC_WIDTH

    # Espaciado base para diferentes tamaños
    if width >= 1200:
        return {
            'header_height': 60,
            'form_padding': 30,
            'field_spacing': 18,
            'input_padding': 12,
            'section_spacing': 25,
            'form_width_ratio': 0.45,  # 45% cada formulario
            'form_gap': 20
        }
    elif width >= 900:
        return {
            'header_height': 55,
            'form_padding': 20,
            'field_spacing': 15,
            'input_padding': 10,
            'section_spacing': 20,
            'form_width_ratio': 0.48,  # 48% cada formulario
            'form_gap': 15
        }
    else:  # Pantallas pequeñas - layout vertical
        return {
            'header_height': 50,
            'form_padding': 15,
            'field_spacing': 12,
            'input_padding': 8,
            'section_spacing': 15,
            'form_width_ratio': 0.9,   # 90% cada formulario
            'form_gap': 10,
            'vertical_layout': True
        }

SPACING = get_responsive_spacing()

# Breakpoints para diseño responsive
BREAKPOINTS = {
    'large': 1200,
    'medium': 900,
    'small': 600
}