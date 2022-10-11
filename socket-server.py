import socket


def server_program():
    # 1st. get the hostname
    host = socket.gethostname()
    port = 5011  # initiate port no above 1024

    # 2. create socket
    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    # 3. bind socket
    server_socket.bind((host, port))  # bind host address and port together

    # 4. listen socket
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    # 5. accept socket -> wait
    conn, address = server_socket.accept()  # accept new connection - return 2 things
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes -> decoding
        data = conn.recv(1024).decode() # 1024: port number
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client -> encoding

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()