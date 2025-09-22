#!/usr/bin/env python3
"""
Create 5 test labels with real USA addresses
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db_manager, Label
from datetime import datetime

def create_usa_test_labels():
    print("=== CREANDO ETIQUETAS DE PRUEBA USA ===")

    try:
        # Connect to database
        if not db_manager.connect():
            print("ERROR: No se pudo conectar a la base de datos")
            return False

        session = db_manager.get_session()
        if not session:
            print("ERROR: No se pudo obtener sesion de base de datos")
            return False

        # USA test addresses data
        test_labels = [
            {
                # Sender 1
                "sender_name": "John Smith",
                "sender_address": "123 Main Street, Apt 4B",
                "sender_city": "New York",
                "sender_state": "NY",
                "sender_zip": "10001",
                # Recipient 1
                "recipient_name": "Mary Johnson",
                "recipient_address": "456 Oak Avenue",
                "recipient_city": "Los Angeles",
                "recipient_state": "CA",
                "recipient_zip": "90210",
                "recipient_tracking": "1Z123456789"
            },
            {
                # Sender 2
                "sender_name": "David Wilson",
                "sender_address": "789 Pine Street, Suite 200",
                "sender_city": "Chicago",
                "sender_state": "IL",
                "sender_zip": "60601",
                # Recipient 2
                "recipient_name": "Sarah Davis",
                "recipient_address": "321 Elm Drive",
                "recipient_city": "Miami",
                "recipient_state": "FL",
                "recipient_zip": "33101",
                "recipient_tracking": "1Z987654321"
            },
            {
                # Sender 3
                "sender_name": "Michael Brown",
                "sender_address": "555 Broadway, Floor 3",
                "sender_city": "Seattle",
                "sender_state": "WA",
                "sender_zip": "98101",
                # Recipient 3
                "recipient_name": "Jennifer Garcia",
                "recipient_address": "777 Cedar Lane",
                "recipient_city": "Austin",
                "recipient_state": "TX",
                "recipient_zip": "73301",
                "recipient_tracking": ""  # Sin tracking
            },
            {
                # Sender 4
                "sender_name": "Lisa Martinez",
                "sender_address": "999 Sunset Boulevard",
                "sender_city": "Las Vegas",
                "sender_state": "NV",
                "sender_zip": "89101",
                # Recipient 4
                "recipient_name": "Robert Lee",
                "recipient_address": "111 Market Street, Unit 15",
                "recipient_city": "San Francisco",
                "recipient_state": "CA",
                "recipient_zip": "94102",
                "recipient_tracking": "1Z456789123"
            },
            {
                # Sender 5
                "sender_name": "Amanda White",
                "sender_address": "222 First Avenue, Building A",
                "sender_city": "Boston",
                "sender_state": "MA",
                "sender_zip": "02101",
                # Recipient 5
                "recipient_name": "Christopher Taylor",
                "recipient_address": "888 Washington Street",
                "recipient_city": "Denver",
                "recipient_state": "CO",
                "recipient_zip": "80201",
                "recipient_tracking": "1Z789123456"
            }
        ]

        created_labels = []

        for i, label_data in enumerate(test_labels, 1):
            try:
                # Create new label
                new_label = Label(
                    user_id=1,  # Assuming admin user has ID 1
                    sender_name=label_data["sender_name"],
                    sender_address=label_data["sender_address"],
                    sender_city=label_data["sender_city"],
                    sender_state=label_data["sender_state"],
                    sender_zip=label_data["sender_zip"],
                    recipient_name=label_data["recipient_name"],
                    recipient_address=label_data["recipient_address"],
                    recipient_city=label_data["recipient_city"],
                    recipient_state=label_data["recipient_state"],
                    recipient_zip=label_data["recipient_zip"],
                    recipient_tracking=label_data["recipient_tracking"],
                    label_type="standard",
                    status="generated",
                    notes=f"Etiqueta de prueba USA #{i}"
                )

                session.add(new_label)
                session.commit()

                created_labels.append(new_label.id)
                print(f"Etiqueta {i} creada (ID: {new_label.id})")
                print(f"  De: {label_data['sender_name']} ({label_data['sender_city']}, {label_data['sender_state']})")
                print(f"  Para: {label_data['recipient_name']} ({label_data['recipient_city']}, {label_data['recipient_state']})")
                if label_data["recipient_tracking"]:
                    print(f"  Tracking: {label_data['recipient_tracking']}")
                else:
                    print(f"  Sin tracking")
                print()

            except Exception as label_error:
                print(f"Error creando etiqueta {i}: {str(label_error)}")
                session.rollback()

        session.close()

        print(f"=== RESUMEN ===")
        print(f"Etiquetas creadas exitosamente: {len(created_labels)}")
        print(f"IDs: {created_labels}")

        return len(created_labels) == 5

    except Exception as e:
        print(f"ERROR GENERAL: {str(e)}")
        return False

if __name__ == "__main__":
    success = create_usa_test_labels()
    if success:
        print("EXITO: Todas las etiquetas de prueba fueron creadas")
    else:
        print("ERROR: No se pudieron crear todas las etiquetas")