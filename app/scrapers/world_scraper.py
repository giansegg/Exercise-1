#  segunda parte 


# import pandas as pd
# from playwright.sync_api import sync_playwright
# from io import StringIO
# import time
# def WorldBankScraper(entity_name):
#     try:
#         with sync_playwright() as p:
#             browser = p.chromium.launch()
#             page = browser.new_page()
#             page.goto("https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms")
            
#             page.wait_for_selector("table tbody tr", timeout=20000)
#             html = page.content()
#             browser.close()

#         df = pd.read_html(StringIO(html))[0]
#         # print("Nombres de las columnas:", df.columns.tolist())

#         # Nos quedamos con el segundo nivel de columnas
#         df.columns = df.columns.droplevel(0)
#         print("datos:", df['Firm Name'].head(20).tolist())


#         # Filtramos usando el nombre correcto de la columna
#         filtered_df = df[df['Firm Name'].str.contains(entity_name, case=False, na=False)]
        
#         if not filtered_df.empty:
#             results = filtered_df[['Firm Name', 'Country', 'To Date', 'Grounds']].to_dict(orient='records')
#             return { 'hits': len(results), 'data': results }
#         else:
#             return { 'hits': 0, 'data': [] }
    
#     except Exception as e:
#         return { 'error': str(e) }


# search_results = WorldBankScraper("entity_name")
# print(search_results)

import pandas as pd
from playwright.sync_api import sync_playwright
import time

def WorldBankScraper(entity_name):
    """
    Versión mínima corregida de tu código original
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()  
            page = browser.new_page()
            
            print("Navegando...")
            page.goto("https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms")
            
            print("Esperando carga...")
            page.wait_for_load_state('domcontentloaded')
            time.sleep(10) 
            
            print("Extrayendo manualmente...")
            data = []
            
            rows = page.query_selector_all('tbody tr, table tr')
            print(f"Filas encontradas: {len(rows)}")
            
            for i, row in enumerate(rows):
                cells = row.query_selector_all('td')
                if len(cells) >= 6:  
                    
                    texts = [cell.inner_text().strip() for cell in cells]
                    
                    if texts[0] and len(texts[0]) > 3 and not texts[0].lower().startswith('firm'):
                        
                        record = {
                            'Firm Name': texts[0],
                            'empty': texts[1] == '',
                            'Address': texts[2] if len(texts) > 2 else '',
                            'Country': texts[3] if len(texts) > 3 else '',
                            'From Date': texts[4] if len(texts) > 4 else '',
                            'To Date': texts[5] if len(texts) > 5 else '',
                            'Grounds': texts[6] if len(texts) > 6 else ''
                        }
                        
                        data.append(record)
                        
                        if i < 5:
                            print(f"  {i+1}. {record['Firm Name']}")
            
            if not data:
                print("Método manual falló, intentando pandas...")
                try:
                    html = page.content()
                    tables = pd.read_html(html)
                    
                    for table in tables:
                        if len(table.columns) >= 6 and len(table) > 1:
                            df = table.copy()
                            
                            if df.columns.nlevels > 1:
                                df.columns = [col[-1] if isinstance(col, tuple) else col for col in df.columns]
                            
                            expected_cols = ['Firm Name', 'Address', 'Country', 'From Date', 'To Date', 'Grounds']
                            df.columns = expected_cols[:len(df.columns)]
                            
                            records = df.to_dict('records')
                            
                            for record in records:
                                firm_name = str(record.get('Firm Name', '')).strip()
                                if firm_name and firm_name != 'nan' and len(firm_name) > 3:
                                    data.append(record)
                            
                            if data:
                                break
                                
                except Exception as e:
                    print(f"Error con pandas: {e}")
            
            browser.close()
            
            print(f"Total extraído: {len(data)} registros")
            
            if entity_name and data:
                filtered = []
                for record in data:
                    firm_name = str(record.get('Firm Name', ''))
                    if entity_name.lower() in firm_name.lower():
                        filtered.append(record)
                
                print(f"Filtrados: {len(filtered)} registros con '{entity_name}'")
                return {'hits': len(filtered), 'data': filtered}
            
            return {'hits': len(data), 'data': data}
            
    except Exception as e:
        print(f"Error: {e}")
        return {'error': str(e)}
