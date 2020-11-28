from socket import *
from http_response_codes import http_responses
import datetime
import os

class Server:
    def __init__(self, hostname='localhost', port=12111, root_directory='./'):
        self.hostname=hostname
        self.port=port

    def run(self):
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(('',self.port))
        server_socket.listen(1)

        print('Server is ready to receive')

        while(1):
            connection_socket, client_addr = server_socket.accept()
            http_request = connection_socket.recv(1024)

            print('Server received the following request' + http_request.decode())
            
            filepath_requested = self.retrieve_file_path(http_request.decode())

            if os.path.exists(filepath_requested):
                
                http_response_header = self.http_respond_builder(200, filepath_requested).encode()
                http_response = http_response_header
                with open(filepath_requested, 'rb') as f:
                    load_bytes = f.read(1024)
                    while (load_bytes):
                        http_response += load_bytes
                        load_bytes = f.read(1024)
                connection_socket.send(http_response)
                
                print('File has been sent')

            else:
                http_response_header = self.http_respond_builder(404).encode()
                connection_socket.send(http_response_header)

                print('File does not exist on server')

            connection_socket.close()
                
    


    def http_respond_builder(self,response_code, filepath="", connection_type='close', http_version='HTTP/1.1'):
        response_line = http_version + " " + str(response_code) + " " + http_responses[response_code]
        connection_type_line = "Connection: " + connection_type
        date_line = "Date: " + str(datetime.datetime.now())

        if filepath != "":
            data_size_line = "Content Length: " + str(os.path.getsize(filepath))
            type_file = "Unknown"
            p, extension = os.path.splitext(filepath)
            if extension == '.txt':
                type_file = "Text"
            content_type_line = "Content-Type: " + type_file
            return response_line + "\n" + connection_type_line + "\n" + date_line + "\n" + \
                data_size_line + "\n" + content_type_line + "\n" + "\n"
        else:
            return response_line + "\n" + connection_type_line + "\n" + date_line + "\n" + "\n"


    

    def retrieve_file_path(self, request):
        request_lines = request.splitlines()
        request_line = request_lines[0].split()
        return request_line[1]
        

if __name__ == "__main__":
    server = Server()
    server.run()