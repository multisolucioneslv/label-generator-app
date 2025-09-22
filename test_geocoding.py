#!/usr/bin/env python3
"""
Test Google Geocoding API for address autocomplete
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import googlemaps
from config import config

def test_geocoding_api():
    print("=== PROBANDO GOOGLE GEOCODING API ===")

    api_key = config.GOOGLE_API_KEY
    if not api_key:
        print("ERROR: No se encontró API Key")
        return False

    print(f"API Key encontrada: {api_key[:15]}...")

    try:
        # Initialize client
        gmaps = googlemaps.Client(key=api_key)

        # Test queries typical for Mexican addresses
        test_queries = [
            "Av Reforma Mexico",
            "Polanco Ciudad Mexico",
            "Santa Fe Mexico DF",
            "Zona Rosa CDMX",
            "Guadalajara Centro"
        ]

        print("\n=== PROBANDO CONSULTAS ===")
        success_count = 0

        for query in test_queries:
            try:
                print(f"\nProbando: '{query}'")

                # Use geocoding (this is what the app actually uses)
                results = gmaps.geocode(
                    address=query + ", Mexico",
                    language='es',
                    region='mx'
                )

                if results:
                    success_count += 1
                    print(f"  EXITO: {len(results)} resultados")

                    # Show first result
                    first_result = results[0]
                    formatted_address = first_result.get('formatted_address', 'N/A')
                    print(f"  Sugerencia: {formatted_address}")

                    # Extract components for analysis
                    components = first_result.get('address_components', [])
                    types = first_result.get('types', [])
                    print(f"  Tipos: {', '.join(types[:3])}")

                else:
                    print(f"  Sin resultados")

            except Exception as e:
                print(f"  ERROR: {str(e)}")

        print(f"\n=== RESUMEN ===")
        print(f"Consultas exitosas: {success_count}/{len(test_queries)}")

        if success_count > 0:
            print("GEOCODING API FUNCIONAL")
            print("El autocompletado deberia funcionar en la aplicacion")
            return True
        else:
            print("GEOCODING API NO FUNCIONAL")
            return False

    except Exception as e:
        print(f"ERROR GENERAL: {str(e)}")

        if "REQUEST_DENIED" in str(e):
            print("\nSOLUCION:")
            print("1. Ve a Google Cloud Console")
            print("2. Habilita 'Geocoding API' (no Places API)")
            print("3. Verifica que la facturacion este activa")
            print("4. Espera 5-10 minutos para que se propague")

        return False

if __name__ == "__main__":
    test_geocoding_api()