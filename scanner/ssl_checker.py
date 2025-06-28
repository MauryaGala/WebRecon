import ssl
import socket
from datetime import datetime

def get_ssl_info(domain):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(3)
            s.connect((domain, 443))
            cert = s.getpeercert()

        issuer = dict(cert['issuer'])
        valid_from = datetime.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z")
        valid_to = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")

        return {
            "valid": valid_to > datetime.now(),
            "issuer": issuer[ssl._OID_NAMES]['organizationName'][0],
            "valid_from": str(valid_from),
            "valid_to": str(valid_to),
            "protocols": s.version()
        }
    except Exception as e:
        return {"error": str(e)}