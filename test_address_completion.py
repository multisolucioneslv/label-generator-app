#!/usr/bin/env python3
"""
Test address autocompletion behavior manually
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import googlemaps
from config import config
from database import db_manager

def test_address_completion():
    print("=== PROBANDO AUTOCOMPLETADO DE DIRECCIONES ===")

    api_key = config.GOOGLE_API_KEY
    if not api_key:
        print("ERROR: No se encontró API Key")
        return False

    print(f"API Key encontrada: {api_key[:15]}...")

    try:
        # Initialize client
        gmaps = googlemaps.Client(key=api_key)

        # Get country setting
        country_name = db_manager.get_setting('default_country', 'USA')
        print(f"País configurado: {country_name}")

        # Test partial addresses that should NOT be replaced with country name
        test_cases = [
            {
                "input": "123 Main",
                "description": "Dirección parcial - debería completar, no reemplazar"
            },
            {
                "input": "Times Sq",
                "description": "Ubicación famosa parcial"
            },
            {
                "input": "Hollywood",
                "description": "Ciudad/área conocida"
            },
            {
                "input": "Broadway",
                "description": "Calle famosa"
            },
            {
                "input": "Wall Street",
                "description": "Dirección específica"
            }
        ]

        print(f"\n=== PROBANDO AUTOCOMPLETADO ===")

        def get_country_code(country_name):
            country_codes = {
                'USA': 'us',
                'Mexico': 'mx',
                'Guatemala': 'gt',
                'El Salvador': 'sv',
                'Honduras': 'hn',
                'Bolivia': 'bo'
            }
            return country_codes.get(country_name, 'us')

        country_code = get_country_code(country_name)

        for test_case in test_cases:
            input_text = test_case["input"]
            description = test_case["description"]

            print(f"\n--- {description} ---")
            print(f"Entrada: '{input_text}'")

            try:
                # Simulate what the app does
                results = gmaps.geocode(
                    address=input_text + f", {country_name}",
                    language='en',
                    region=country_code
                )

                if results:
                    print(f"Resultados encontrados: {len(results)}")

                    for i, result in enumerate(results[:3]):  # Show top 3
                        formatted_address = result.get('formatted_address', '')
                        print(f"  {i+1}. {formatted_address}")

                        # Simulate the cleaning process
                        clean_suggestion = formatted_address
                        country_suffixes = [", USA", ", Mexico", ", Guatemala", ", El Salvador", ", Honduras", ", Bolivia"]
                        for suffix in country_suffixes:
                            if suffix in clean_suggestion:
                                clean_suggestion = clean_suggestion.split(suffix)[0]

                        print(f"     Limpio: {clean_suggestion}")

                        # Check if it would be a good suggestion
                        if (input_text.lower() in clean_suggestion.lower() or
                            clean_suggestion.lower().startswith(input_text.lower())):
                            print(f"     BUENA SUGERENCIA")
                        else:
                            print(f"     No es buena sugerencia")

                        # Check if it would be blocked
                        country_names = ["USA", "United States", "Mexico", "Guatemala", "El Salvador", "Honduras", "Bolivia"]
                        if any(country.lower() in clean_suggestion.lower() and len(clean_suggestion) < 30 for country in country_names):
                            print(f"     BLOQUEADA (solo pais)")

                else:
                    print("  Sin resultados")

            except Exception as e:
                print(f"  ERROR: {str(e)}")

        print(f"\n=== CONCLUSION ===")
        print("El autocompletado deberia:")
        print("+ Completar direcciones parciales especificas")
        print("- NO reemplazar con solo nombres de paises")
        print("+ Limpiar sufijos de paises de las sugerencias")
        print("+ Solo sugerir si la entrada coincide con el resultado")

        return True

    except Exception as e:
        print(f"ERROR GENERAL: {str(e)}")
        return False

if __name__ == "__main__":
    test_address_completion()