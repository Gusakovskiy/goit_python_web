from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, get!')

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, post!')


if __name__ == '__main__':
    server_address = ('127.0.0.1', 5000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()
