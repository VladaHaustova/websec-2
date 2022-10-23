import http.server
import socket
from html_parser import getHTML

class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

def start_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 2000))
        server.listen(4)
        while True:
            print('Server working...')
            client_socket, address = server.accept()
            getHTML()
            data = client_socket.recv(1024).decode('utf-8')
            content = load_page_from_get_request(data)
            client_socket.send(content)
            client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()
        print('Server is shutdown')


def load_page_from_get_request(request_data):
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'

    if len(request_data.split(' ')) < 2:
        return (HDRS_404 + 'Sorry').encode('utf-8')
    path = request_data.split(' ')[1]
    response = ''
    try:
        with open('schedule_client' + path, 'rb') as file:
            response = file.read()

        if path == "/style.css":
            HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/css; charset=utf-8\r\n\r\n'
        if path == "/script.js":
            HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/javascript; charset=utf-8\r\n\r\n'
        if path == "/schedule.txt":
            HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: application/json; charset=utf-8\r\n\r\n'
        return HDRS.encode('utf-8') + response
    except FileNotFoundError:
        return(HDRS_404 + 'Sorry').encode('utf-8')

if __name__ == "__main__":
    start_server()