import requests

def get_http_headers(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        resp = requests.get(url, timeout=5)
        return resp.headers
    except Exception as e:
        return {"error": str(e)}