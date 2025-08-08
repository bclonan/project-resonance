# benchmarks/system/resonance_balancer.py
import os
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys

# Add project root to path to import our library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from phiresearch_systems import PhiBalancer

# Validate and parse backend hosts from environment
backend_hosts_env = os.getenv("BACKEND_HOSTS", "localhost:8001")
if not backend_hosts_env.strip():
    raise ValueError("BACKEND_HOSTS environment variable cannot be empty")

BACKEND_HOSTS = [host.strip() for host in backend_hosts_env.split(',') if host.strip()]
if not BACKEND_HOSTS:
    raise ValueError("No valid backend hosts found in BACKEND_HOSTS environment variable")

BALANCER = PhiBalancer([f"http://{host}" for host in BACKEND_HOSTS])

class ResonanceProxy(BaseHTTPRequestHandler):
    def do_GET(self):
        # Use the client's IP address as the request ID for routing
        request_id = self.client_address[0]
        backend_url = BALANCER.get_server_for_request(request_id)
        
        try:
            res = requests.get(f"{backend_url}{self.path}", timeout=5)
            self.send_response(res.status_code)
            for key, value in res.headers.items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(res.content)
        except requests.exceptions.RequestException as e:
            self.send_error(503, f"Service Unavailable: {e}")

if __name__ == "__main__":
    server_address = ('', 80)
    httpd = HTTPServer(server_address, ResonanceProxy)
    print(f"Resonance Balancer running on port 80, routing to: {BACKEND_HOSTS}")
    httpd.serve_forever()