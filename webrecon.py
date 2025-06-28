import argparse
from scanner.port_scanner import scan_ports
from scanner.ssl_checker import get_ssl_info
from scanner.http_headers import get_http_headers
from scanner.vuln_checker import check_vulns

def main():
    parser = argparse.ArgumentParser(description="Web Reconnaissance Tool - Scan Open Ports, SSL Info, Headers & Basic Web Vulnerabilities")
    parser.add_argument("target", help="Domain or IP address to scan (e.g., example.com)")
    args = parser.parse_args()
    target = args.target

    print(f"\n[+] Scanning {target}...\n")

    # Port Scan
    print("[*] Scanning common ports...")
    open_ports = scan_ports(target)
    print(f"Open Ports: {open_ports}")

    # SSL Check (if HTTPS is open)
    if 443 in open_ports:
        print("\n[*] Checking SSL Certificate...")
        ssl_info = get_ssl_info(target)
        for k, v in ssl_info.items():
            print(f"{k}: {v}")

    # HTTP Headers
    print(f"\n[*] Fetching HTTP Headers from http://{target}...")
    headers = get_http_headers(target)
    if "error" in headers:
        print(f"[!] Error fetching headers: {headers['error']}")
    else:
        for k, v in headers.items():
            print(f"{k}: {v}")

    # Vulnerability Check
    print("\n[*] Checking for basic web vulnerabilities...")
    vulns = check_vulns(headers)
    for vuln, found in vulns.items():
        print(f"[!] {vuln} vulnerability {'found' if found else 'not found'}")

if __name__ == "__main__":
    main()