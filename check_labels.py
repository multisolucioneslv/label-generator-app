import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db_manager, Label, User

def check_labels():
    print("=== VERIFICANDO ETIQUETAS EN BASE DE DATOS ===")

    try:
        db_manager.connect()
        session = db_manager.get_session()

        # Contar etiquetas
        total_labels = session.query(Label).count()
        print(f"Total de etiquetas: {total_labels}")

        if total_labels > 0:
            print("\n=== HISTORIAL DE ETIQUETAS ===")

            labels = session.query(Label).order_by(Label.created_at.desc()).all()

            for i, label in enumerate(labels, 1):
                print(f"\n{i}. Etiqueta ID: {label.id}")
                print(f"   De: {label.sender_name} ({label.sender_city})")
                print(f"   Para: {label.recipient_name} ({label.recipient_city})")
                if label.recipient_tracking:
                    print(f"   Tracking: {label.recipient_tracking}")
                print(f"   Creada: {label.created_at}")
                print(f"   Estado: {label.status}")

        # Verificar usuarios
        total_users = session.query(User).count()
        print(f"\n=== USUARIOS ===")
        print(f"Total de usuarios: {total_users}")

        users = session.query(User).all()
        for user in users:
            status = "Activo" if user.is_active else "Inactivo"
            role = "Admin" if user.is_admin else "Usuario"
            print(f"- {user.username} ({user.full_name}) - {role} - {status}")

        session.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_labels()