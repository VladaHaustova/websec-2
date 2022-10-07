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
        server.listen(4)  # кол-во входящих запросов
        while True:
            print('Server working...') # ожидание
            client_socket, address = server.accept()
            getHTML()
            data = client_socket.recv(1024).decode('utf-8') # получаем содержимое запроса
            content = load_page_from_get_request(data) # обработка запроса
            client_socket.send(content) # ответ
            client_socket.shutdown(socket.SHUT_WR) # закрываем соединение с клиентом после того, как был отправлен ответ
    except KeyboardInterrupt:
        server.close()
        print('Server is shutdown')

# def open_files(path, path_name, content_type):
    # if path == path_name:
        # HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: {content_type}; charset=utf-8\r\n\r\n'

def load_page_from_get_request(request_data): # обработка запроса клиента
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'

    if len(request_data.split(' ')) < 2:
        return (HDRS_404 + 'Sorry').encode('utf-8')
    path = request_data.split(' ')[1]
    response = ''
    try:
        with open('schedule_client' + path, 'rb') as file:
            response = file.read()

        # open_files(path, "/style.css", 'text/css')
        # open_files(path, "/script.js", 'text/javascript')
        # open_files(path, "/schedule.txt", 'content_type')

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