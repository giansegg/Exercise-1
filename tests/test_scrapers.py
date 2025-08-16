
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.scrapers.offshore_scraper import OffshoreScrapper

def run_test():
    
    scraper = OffshoreScrapper()
    entity_name = "Miranda & Amado | Lima, Peru"  
    
    try:
        results = scraper.search_entity(entity_name)
        
        if results:
            print("se encontraron los siguientes resultados :")
            for item in results:
                print(f"  - Nombre: {item.get('Entity')}")
                print(f"    - Jurisdicción: {item.get('Jurisdiction')}")
                print(f"    - Vinculado a: {item.get('Linked To')}")
                print(f"    - Incorporado: {item.get('Incorporated')}")
                print(f"    - Cerrado: {item.get('Closed')}")
                print(f"    - Inactivación: {item.get('Inactivation')}")
                print(f"    - Eliminado: {item.get('Struck off')}")
                print(f"    - Estado: {item.get('Status')}")
            print("\nPrueba finalizada.")
        else:
            print(" faill. No se encontraron resultados.")
            
    except Exception as e:
        print(f" La prueba fallo debido a un error: {e}")

if __name__ == "__main__":
    run_test()