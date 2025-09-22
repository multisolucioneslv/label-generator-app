#!/usr/bin/env python3
"""
Set default country to USA in database
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db_manager

def set_default_country():
    print("=== CONFIGURANDO PAIS PREDETERMINADO ===")

    try:
        # Connect to database
        if not db_manager.connect():
            print("ERROR: No se pudo conectar a la base de datos")
            return False

        # Set USA as default country
        success = db_manager.set_setting('default_country', 'USA')

        if success:
            print("EXITO: Pais predeterminado configurado a USA")

            # Verify setting
            current_country = db_manager.get_setting('default_country')
            print(f"Verificacion: Pais actual = {current_country}")

            return True
        else:
            print("ERROR: No se pudo guardar la configuracion")
            return False

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    set_default_country()