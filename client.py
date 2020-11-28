from socket import *
from http_response_codes import http_responses

class Client:
      

    def request_file(self, hostname, port, filepath):
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((hostname, port))
        request = self.http_request_builder(filepath, hostname)

        client_socket.send(request.encode('utf-8'))
        response = client_socket.recv(2048)
        
        output_path = input('Where would you like to save file? (type \'no\'to display the file: ')
        if output_path == 'no':
            print(response)
        else:
            self.write_to_file(output_path, response)
        
        client_socket.close()
    
    def http_request_builder(self, filepath, hostname, connection_type='close', request_type='GET', http_version='HTTP/1.1'):
        request_line = request_type + " " + filepath + " " + http_version
        host_line = "Host: " + hostname
        connection_type_line = "Connection: " + connection_type
        return request_line + "\n" + host_line + "\n" + connection_type_line

    def write_to_file(self, output_path, response):
        result, file_data = self.get_bytes_from_response(response)

        if result:
            try: 
                with open(output_path, 'w+') as f:
                    f.write(file_data)
                print("\nSuccessfully saved to " + output_path)    
            except:
                print("\nNot successfully saved to " + filepath)
        else:
            print("Server returns error code: " + file_data) 

    def get_bytes_from_response(self, response):
        string_response = response.decode()

        parts = string_response.split('\n\n')

        code = int(parts[0].split('\n')[0].split()[1]) 

        if code == 200:
            return True, parts[1]
        else:
            return False, str(code)




        





if __name__ == "__main__":
    client = Client()

    filepath = input('Please enter path name: ')

    client.request_file('localhost', 12111, filepath)