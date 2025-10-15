from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse


PORT = 8000


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {
            '/': 'index.html',
            '/index.html': 'index.html',
            '/catalog.html': 'catalog.html',
            '/contacts.html': 'contacts.html',
            '/category.html': 'category.html',
        }
        filepath = routes.get(self.path, None)
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(b'404: File not found')
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'404: File not found')

    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = urllib.parse.parse_qs(post_data)
            print("Получены данные POST-запроса:")
            for key, values in parsed_data.items():
                print(f"{key}: {values}")

            response = ('<html><body>'
                        '<h1>Спасибо за отправку формы!</h1>'
                        '<a href="/contacts.html">Вернуться на страницу Контакты</a>'
                        '</body></html>')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на http://localhost:{PORT}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()