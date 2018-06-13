import os
import socketserver


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        pass


server = socketserver.ThreadingTCPServer(("127.0.0.1", "1234"), MyServer)
server.serve_forever()


URL = "put|D:\\Mike\\PythonCode\\练习\\untitled\\Test.py"

cmd, path = URL.split("|")
print(cmd)
print(path)

base_dir = os.path.dirname(os.path.abspath(__file__))
print(base_dir)

# path = os.path.join(base_dir, path)
# print(path)

filename = os.path.basename(path)
print(filename)

file_size = os.stat(path).st_size
print(file_size)

