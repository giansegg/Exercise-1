import re

def is_valid_entity_name(name: str) -> bool:
    
    if not isinstance(name, str) or not name.strip():
        return False
        
    if len(name.strip()) < 2:
        return False
        
    safe_pattern = re.compile(r"^[a-zA-Z0-9\s&,.'-]+$")
    if not safe_pattern.match(name):
        return False

    return True

def is_valid_url(url: str) -> bool:

    if not isinstance(url, str) or not url.strip():
        return False
        
    url_pattern = re.compile(r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$')
    return url_pattern.match(url)

def is_valid_integer(value: any) -> bool:
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False