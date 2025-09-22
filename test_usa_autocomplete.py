#!/usr/bin/env python3
"""
Test USA address autocomplete functionality
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import googlemaps
from config import config
from database import db_manager

def test_usa_autocomplete():
    print("=== PROBANDO AUTOCOMPLETADO USA ===")

    api_key = config.GOOGLE_API_KEY
    if not api_key:
        print("ERROR: No se encontró API Key")
        return False

    print(f"API Key encontrada: {api_key[:15]}...")

    try:
        # Initialize client
        gmaps = googlemaps.Client(key=api_key)

        # Verify country setting
        country_setting = db_manager.get_setting('default_country', 'USA')
        print(f"País configurado: {country_setting}")

        # Test USA addresses
        test_queries = [
            "123 Main Street",
            "Times Square New York",
            "Hollywood Los Angeles",
            "Miami Beach Florida",
            "Chicago Downtown"
        ]

        print("\n=== PROBANDO DIRECCIONES USA ===")
        success_count = 0

        for query in test_queries:
            try:
                print(f"\nProbando: '{query}'")

                # Use geocoding with USA as country
                results = gmaps.geocode(
                    address=query + ", USA",
                    language='en',
                    region='us'
                )

                if results:
                    success_count += 1
                    print(f"  EXITO: {len(results)} resultados")

                    # Show first result
                    first_result = results[0]
                    formatted_address = first_result.get('formatted_address', 'N/A')
                    print(f"  Sugerencia: {formatted_address}")

                else:
                    print(f"  Sin resultados")

            except Exception as e:
                print(f"  ERROR: {str(e)}")

        print(f"\n=== RESUMEN ===")
        print(f"Consultas exitosas: {success_count}/{len(test_queries)}")

        if success_count > 0:
            print("AUTOCOMPLETADO USA FUNCIONAL")
            return True
        else:
            print("AUTOCOMPLETADO USA NO FUNCIONAL")
            return False

    except Exception as e:
        print(f"ERROR GENERAL: {str(e)}")
        return False

if __name__ == "__main__":
    test_usa_autocomplete()