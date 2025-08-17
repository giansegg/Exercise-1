from flask import Blueprint, request, jsonify
from app.scrapers.offshore_scraper import OffshoreScraper
from app.scrapers.world_scraper import WorldBankScraper
from .responses import success_response, error_response
from ..utils.validators import is_valid_entity_name


api_bp = Blueprint('api', __name__)

@api_bp.route('/search', methods=['GET'])
def search_entities():
    entity_name = request.args.get('entity_name')

    is_valid, error_msg = is_valid_entity_name(entity_name)
    if not is_valid:
        return error_response(400, error_msg)
        
    try:
        all_results = []
        sources_found = []

        # scraper 1
        offshore_scraper = OffshoreScraper()
        offshore_results = offshore_scraper.search_entity(entity_name)
        if 'error' in offshore_results:
            print(f'Offshore Leaks Scraper Error : ', offshore_results['error'])
        elif offshore_results.get('data'):
            all_results.extend(offshore_results['data'])
            sources_found.append("Offshore Leaks")

        # scraper 2
        world_scraper_output = WorldBankScraper(entity_name)
        if 'error' in world_scraper_output:
            print(f'World Bank Scraper Error : ', world_scraper_output['error'])
        elif world_scraper_output.get('data'):
            all_results.extend(world_scraper_output['data'])
            sources_found.append("The World Bank")

        hits = len(all_results)
        if hits == 0:
            return error_response(200, f"No se encontraron resultados para: {entity_name}")

        response_data = {
            "hits": hits,
            "sources_found": sources_found,
            "results": all_results
        }
        return success_response(200, "Búsqueda completada exitosamente.", response_data)

    except Exception as e:
        return error_response(500, f"Ocurrió un error interno: {str(e)}")