import http.server
import socketserver
import urllib.parse
import os

PORT = 8888
DIRECTORY = "/home/temisotis/Projetos/vanessa-efeito-caracois/metodo-caracois-v1"

class NetlifyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Remove query parameters for normal file check
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Check if it is a Netlify image request
        if parsed_path.path == '/.netlify/images':
            query = urllib.parse.parse_qs(parsed_path.query)
            if 'url' in query:
                # Redirect to the local image path
                local_image_path = query['url'][0]
                self.path = local_image_path
                return super().do_GET()
        
        return super().do_GET()

with socketserver.TCPServer(("", PORT), NetlifyHandler) as httpd:
    print(f"Servidor Método Completo rodando em http://localhost:{PORT}")
    httpd.serve_forever()
