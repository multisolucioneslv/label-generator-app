import tkinter as tk
from tkinter import ttk
from config.settings import COLORS, FONTS, SPACING

class FormFieldsComponent:
    def __init__(self):
        self.form_fields = {}

    def create_modern_form_fields(self, parent_frame, form_type, accent_color):
        # Contenedor principal responsive
        fields_frame = tk.Frame(parent_frame, bg=COLORS['white'])
        fields_frame.pack(padx=SPACING['form_padding'], pady=SPACING['field_spacing'], fill="both", expand=True)

        # Estilo para campos de entrada mejorado
        entry_style = {
            "font": FONTS['input'],
            "relief": "solid",
            "bd": 1,
            "highlightthickness": 2,
            "highlightcolor": accent_color,
            "highlightbackground": COLORS['border'],
            "bg": COLORS['white'],
            "fg": COLORS['text_primary']
        }

        # Campo Nombre - responsive
        nombre_container = self._create_field_container(fields_frame, "👤 Nombre completo")
        nombre_entry = tk.Entry(nombre_container, **entry_style)
        self._add_placeholder_animation(nombre_entry, "Ingrese el nombre completo")
        nombre_entry.pack(fill="x", ipady=SPACING['input_padding'])

        # Campo Dirección - responsive
        direccion_container = self._create_field_container(fields_frame, "🏠 Dirección")
        direccion_entry = tk.Entry(direccion_container, **entry_style)
        self._add_placeholder_animation(direccion_entry, "Calle, número, colonia...")
        direccion_entry.pack(fill="x", ipady=SPACING['input_padding'])

        # Ubicación en grid optimizada
        location_label = tk.Label(fields_frame, text="📍 Ubicación",
                                bg=COLORS['white'], fg=COLORS['text_secondary'],
                                font=FONTS['label'])
        location_label.pack(anchor="w", pady=(SPACING['field_spacing'], 3))

        location_frame = tk.Frame(fields_frame, bg=COLORS['white'])
        location_frame.pack(fill="x", pady=(0, SPACING['field_spacing']))

        # Grid 2x2 para mejor uso del espacio
        # Fila 1: Ciudad y Estado
        row1_frame = tk.Frame(location_frame, bg=COLORS['white'])
        row1_frame.pack(fill="x", pady=(0, 8))

        ciudad_entry = self._create_compact_field(row1_frame, "Ciudad", "Ciudad", entry_style, side="left")
        estado_entry = self._create_compact_field(row1_frame, "Estado", "Estado", entry_style, side="right")

        # Fila 2: ZIP (centrado y más pequeño)
        row2_frame = tk.Frame(location_frame, bg=COLORS['white'])
        row2_frame.pack(fill="x")

        zip_frame = tk.Frame(row2_frame, bg=COLORS['white'])
        zip_frame.pack()

        zip_label = tk.Label(zip_frame, text="Código Postal",
                           bg=COLORS['white'], fg=COLORS['text_muted'],
                           font=FONTS['small'])
        zip_label.pack()
        zip_entry = tk.Entry(zip_frame, width=15, **entry_style)
        self._add_placeholder_animation(zip_entry, "00000")
        zip_entry.pack(ipady=SPACING['input_padding']-2)

        # Mini progress indicator responsive
        progress_frame = tk.Frame(fields_frame, bg=COLORS['white'])
        progress_frame.pack(fill="x", pady=(SPACING['field_spacing'], 0))

        # Ancho de barra de progreso adaptativo
        progress_width = min(300, int(SPACING.get('form_width_ratio', 0.8) * 400))
        progress_bar = ttk.Progressbar(progress_frame, length=progress_width, mode='determinate')
        progress_bar.pack()
        progress_bar['value'] = 0

        # Guardar referencias
        self.form_fields[form_type] = {
            'nombre': nombre_entry,
            'direccion': direccion_entry,
            'ciudad': ciudad_entry,
            'estado': estado_entry,
            'zip': zip_entry,
            'progress': progress_bar
        }

        # Vincular eventos para progreso
        for field in [nombre_entry, direccion_entry, ciudad_entry, estado_entry, zip_entry]:
            field.bind('<KeyRelease>', lambda e, t=form_type: self.update_progress(t))
            field.bind('<FocusOut>', lambda e, t=form_type: self.update_progress(t))

        return fields_frame

    def _create_field_container(self, parent, label_text):
        container = tk.Frame(parent, bg=COLORS['white'])
        container.pack(fill="x", pady=(0, SPACING['field_spacing']))

        label = tk.Label(container, text=label_text,
                        bg=COLORS['white'], fg=COLORS['text_secondary'],
                        font=FONTS['label'])
        label.pack(anchor="w", pady=(0, 3))

        return container

    def _create_compact_field(self, parent, label_text, placeholder, entry_style, side):
        frame = tk.Frame(parent, bg=COLORS['white'])
        if side == "left":
            frame.pack(side="left", fill="x", expand=True, padx=(0, 8))
        else:
            frame.pack(side="right", fill="x", expand=True, padx=(8, 0))

        label = tk.Label(frame, text=label_text,
                        bg=COLORS['white'], fg=COLORS['text_muted'],
                        font=FONTS['small'])
        label.pack(anchor="w")

        entry = tk.Entry(frame, **entry_style)
        self._add_placeholder_animation(entry, placeholder)
        entry.pack(fill="x", ipady=SPACING['input_padding']-2)

        return entry

    def _add_placeholder_animation(self, entry, placeholder_text):
        entry.placeholder_text = placeholder_text
        entry.placeholder_active = True

        def on_focus_in(event):
            if entry.placeholder_active:
                entry.delete(0, tk.END)
                entry.config(fg=COLORS['text_primary'])
                entry.placeholder_active = False

        def on_focus_out(event):
            if not entry.get():
                entry.placeholder_active = True
                entry.insert(0, placeholder_text)
                entry.config(fg=COLORS['placeholder'])

        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

        # Configurar placeholder inicial
        entry.insert(0, placeholder_text)
        entry.config(fg=COLORS['placeholder'])

    def update_progress(self, form_type):
        if form_type in self.form_fields:
            fields = self.form_fields[form_type]
            filled_fields = 0
            total_fields = 5

            for field_name, field_widget in fields.items():
                if field_name != 'progress' and field_widget.get() and not field_widget.placeholder_active:
                    filled_fields += 1

            progress_percentage = (filled_fields / total_fields) * 100
            fields['progress']['value'] = progress_percentage

    def get_form_data(self, form_type):
        if form_type in self.form_fields:
            data = {}
            for field, widget in self.form_fields[form_type].items():
                if field != 'progress':
                    data[field] = widget.get() if not widget.placeholder_active else ""
            return data
        return {}