from .base_scraper import BaseScraper
from bs4 import Tag

class OffshoreScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://offshoreleaks.icij.org")
    

    # def extract_entity_info(self, soup):
    #     entity_info = []
    #     results = soup.find_all('div', class_='search__results__content')
    #     for result in results:
    #         link_tag = result.find('a')
    #         if link_tag and 'href' in link_tag.attrs:
    #             entity_name = link_tag.text.strip()
    #             entity_url = link_tag['href']
    #             if not entity_url.startswith('http'):
    #                 entity_url = f"{self.base_url}{entity_url}"
    #             entity_info.append({
    #                 'name': entity_name,
    #                 'url': entity_url
    #             })
            
    #     return entity_info
    
    def scrape_details_page(self, details_url):
        print(f"DEBUG: Scrapeando página de detalles: {details_url}")

        html_content = self.get_pageContent(details_url)
        if not html_content:
            return {}
        soup = self.parse_html(html_content)
        if not soup:
            return {}
        details = {
             'Entity': None,
            'Jurisdiction': None,
            'Linked To': None,
            'Data From': None,
            'Incorporated': None,
            'Inactivation': None,
            'Struck off': None,
            'Status': None
        }
        entity_name_tag = soup.find('h1', class_='node__content__header__name')
        if entity_name_tag:
            details['Entity'] = entity_name_tag.get_text(strip=True)

        jurisdiction_label = soup.find('div', class_='metadata__properties__row__attribute-type', string=lambda text: 'Registered in:' in text)
        if jurisdiction_label:
            jurisdiction_value_tag = jurisdiction_label.find_next_sibling('div', class_='metadata__properties__row__attribute-value')
            if jurisdiction_value_tag:
                jurisdiction_link = jurisdiction_value_tag.find('a')
                details['Jurisdiction'] = jurisdiction_link.get_text(strip=True) if jurisdiction_link else jurisdiction_value_tag.get_text(strip=True)

        linked_to_label = soup.find('div', class_='metadata__properties__row__attribute-type', string=lambda text: 'Linked countries:' in text)
        if linked_to_label:
            linked_to_value_tag = linked_to_label.find_next_sibling('div', class_='metadata__properties__row__attribute-value')
            if linked_to_value_tag:
                linked_countries = [a.get_text(strip=True) for a in linked_to_value_tag.find_all('a')]
                details['Linked To'] = ", ".join(linked_countries)


        data_from_tag = soup.find('div', class_='node__content__category')
        if data_from_tag:
            details['Data From'] = data_from_tag.get_text(strip=True).replace('Entity:', '').strip()
        
        dates_container = soup.find('div', class_='metadata__dates')
        if dates_container:
            incorporated_tag = dates_container.find('div', class_='metadata__dates__date-type', string=lambda text: 'Incorporated:' in text)
            if incorporated_tag:
                date_value = incorporated_tag.find_next_sibling('div', class_='metadata__dates__date-value')
                details['Incorporated'] = date_value.get_text(strip=True) if date_value else None
            
            inactivation_tag = dates_container.find('div', class_='metadata__dates__date-type', string=lambda text: 'Inactivation:' in text)
            if inactivation_tag:
                date_value = inactivation_tag.find_next_sibling('div', class_='metadata__dates__date-value')
                details['Inactivation'] = date_value.get_text(strip=True) if date_value else None

            close_tag = dates_container.find('div', class_='metadata__dates__date-type', string=lambda text: 'Closed:' in text)
            if close_tag:
                date_value = close_tag.find_next_sibling('div', class_='metadata__dates__date-value')
                details['Closed'] = date_value.get_text(strip=True) if date_value else None

            struck_off_tag = dates_container.find('div', class_='metadata__dates__date-type', string=lambda text: 'Struck off:' in text)
            if struck_off_tag:
                date_value = struck_off_tag.find_next_sibling('div', class_='metadata__dates__date-value')
                details['Struck off'] = date_value.get_text(strip=True) if date_value else None
            
            status_tag = dates_container.find('div', class_='metadata__dates__status')
            if status_tag:
                status_value = status_tag.find_next_sibling('div', class_='metadata__dates__status-value')
                details['Status'] = status_value.get_text(strip=True) if status_value else None
        print(f"DEBUG: Detalles extraídos: {details}")

        
        return details

        
        
    def search_entity(self, entity_name):
        print(f"DEBUG: Iniciando búsqueda para la entidad: {entity_name}")

        search_url = f"{self.base_url}/search?q={entity_name}"
        html_content = self.get_pageContent(search_url)
        if not html_content:
            return {"hits": 0, "data": []}
        soup = self.parse_html(html_content)
        if not soup:
            return {"hits": 0, "data": []}

        result_div = soup.find('table', class_='search__results__table')
        if not result_div:
            return {"hits": 0, "data": []}

        results_with_links = []
        rows = result_div.find('tbody').find_all('tr')
        print(f"DEBUG: Se encontraron {len(rows)} filas de resultados.")


        rows_top_5 = rows[:5]
        print(f"DEBUG: Procesando las primeras {len(rows_top_5)} filas.")


        for row in rows_top_5:
            td_tag = row.find('td')
            if td_tag:
                link_tag = row.find('a', href=True)
                if link_tag:
                    entity_name = link_tag.get_text(strip=True)
                    details_url = f"{self.base_url}{link_tag['href']}"

                    results_with_links.append({
                        'name': entity_name,
                        'url': details_url
                    })

        final_results = []
        for item in results_with_links:
            details = self.scrape_details_page(item['url'])
            final_results.append({
                "Entity": item['name'],
                **details
            })
            self.sleep(1) 

        return {
            "hits": len(final_results),
            "data": final_results
        }
