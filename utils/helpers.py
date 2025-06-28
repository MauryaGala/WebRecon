def format_headers(headers):
    """Format HTTP headers for cleaner output"""
    formatted = {}
    for key, value in headers.items():
        formatted[key] = value
    return formatted