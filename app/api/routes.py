from flask import Blueprint, request, jsonify
from app.scrapers.offshore_scraper import OffshoreScrapper
from api.responses import success_response, error_response
from utils.validators import is_valid_entity_name


api_bp = Blueprint('api', __name__)

@api_bp.route('/search', methods=['GET'])
def search_entities():
    entity_name = request.args.get('entity_name')

    if not is_valid_entity_name(entity_name):
        return error_response(400, "Nombre de entidad no válido. El nombre debe ser una cadena no vacía, tener al menos 2 caracteres y contener solo letras, números, espacios y caracteres como '&,.-'")
        
    try:
        all_results = []
        sources_found = []
        # scraper 1
        offshore_scraper = OffshoreScrapper()
        offshore_results = offshore_scraper.search_entity(entity_name)
        if offshore_results:
            all_results.extend(offshore_results)
            sources_found.append("Offshore Leaks")

        # scraper 2
        # world_scraper = WorldScraper()
        # world_results = world_scraper.search_entity(entity_name)
        # if world_results:
        #     all_results.extend(world_results)
        #     sources_found.append("The World Bank")

        # scraper 3
        # ofac_scraper = OfacScraper()
        # ofac_results = ofac_scraper.search_entity(entity_name)
        # if ofac_results:
        #     all_results.extend(ofac_results)
        #     sources_found.append("OFAC")

        hits = len(all_results)
        if hits == 0:
            return error_response(404, f"No se encontraron resultados para: {entity_name}")

        response_data = {
            "hits": hits,
            "sources_found": sources_found,
            "results": all_results
        }
        return success_response(200, "Búsqueda completada exitosamente.", response_data)

    except Exception as e:
        return error_response(500, f"Ocurrió un error interno: {str(e)}")