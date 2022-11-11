import socket
from html_parser import getHTML, getGroups, getAndSaveTeachers

tmpp = ""

def start_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 2000))
        server.listen(4)
        # getAndSaveTeachers()
        while True:
            path = "/"
            print('Server working...')
            client_socket, address = server.accept()
            data = client_socket.recv(1024).decode('utf-8')

            if len(data.split(' ')) > 1:
                path = data.split(' ')[1]
            # print(path)
            if path == "/":
                HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
                with open('schedule_client/index.html', 'rb') as file:
                    response = file.read()
                client_socket.send(HDRS.encode('utf-8') + response)
                client_socket.shutdown(socket.SHUT_WR)
                continue
            elif path == "/script.js":
                HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/javascript; charset=utf-8\r\n\r\n'
                with open('schedule_client/script.js', 'rb') as file:
                    response = file.read()
                client_socket.send(HDRS.encode('utf-8') + response)
                client_socket.shutdown(socket.SHUT_WR)
                continue
            elif path == "/style.css":
                HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/css; charset=utf-8\r\n\r\n'
                with open('schedule_client/style.css', 'rb') as file:
                    response = file.read()
                client_socket.send(HDRS.encode('utf-8') + response)
                client_socket.shutdown(socket.SHUT_WR)
                continue
            elif path == "/groups":
                HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: application/json; charset=utf-8\r\n\r\n'
                response = getGroups()
                client_socket.send(HDRS.encode('utf-8') + response.encode('utf-8'))
                client_socket.shutdown(socket.SHUT_WR)
                continue
            elif path == "/teachers":
                HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: application/json; charset=utf-8\r\n\r\n'
                with open('schedule_client/teachers.txt', 'rb') as file:
                    response = file.read()
                client_socket.send(HDRS.encode('utf-8') + response)
                client_socket.shutdown(socket.SHUT_WR)
                continue

            HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: application/json; charset=utf-8\r\n\r\n'
            response = getHTML(path)
            client_socket.send(HDRS.encode('utf-8') + response.encode('utf-8'))
            client_socket.shutdown(socket.SHUT_WR)

    except KeyboardInterrupt:
        server.close()
        print('Server is shutdown')


if __name__ == "__main__":
    start_server()