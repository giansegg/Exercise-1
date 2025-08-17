import re

def is_valid_entity_name(name: str) -> tuple[bool, str]:
    
    if not isinstance(name, str) or not name.strip():
        return False, "La entidad no puede estar vacía."

    if len(name.strip()) < 2:
        return False, "El nombre de la entidad es demasiado corto."
    if len(name.strip()) > 150:
        return False, "El nombre de la entidad es demasiado largo."

    safe_pattern = re.compile(r"^[a-zA-Z0-9\s&,.'-]+$")
    if not safe_pattern.match(name):
        return False, "El nombre de la entidad contiene caracteres no válidos."

    return True, ""

def is_valid_url(url: str) -> tuple[bool, str]:

    if not isinstance(url, str) or not url.strip():
        return False, "URL inválida."

    url_pattern = re.compile(r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$')
    return url_pattern.match(url)

def is_valid_integer(value: any) -> tuple[bool, str]:
    try:
        int(value)
        return True, ""
    except (ValueError, TypeError):
        return False, "El valor debe ser un numero entero válido."