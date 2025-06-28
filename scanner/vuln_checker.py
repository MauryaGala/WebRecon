def check_vulns(headers):
    vulns = {}

    vulns["Clickjacking"] = "X-Frame-Options" not in headers
    vulns["XSS Protection"] = headers.get("X-XSS-Protection") != "1; mode=block"
    vulns["Missing CSP"] = "Content-Security-Policy" not in headers
    vulns["HSTS"] = "Strict-Transport-Security" not in headers

    return vulns