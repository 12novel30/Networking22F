'''
in 22-10-13 in lecture
- 이런 파일 만들어보고/수정해보는 것 final project에 도움될 것
- 뭘 주고받는지 모르겠으면 print() 다 찍어보기
'''

import select, socket, sys, queue

host = socket.gethostname()
server = socket.socket()  # get instance
server.setblocking(0)  

# binding
server.bind((host, 50000))
# 5개의 소켓  
server.listen(5) 
inputs = [server]
outputs = []
message_queues = {}

while inputs:
    '''main diff [select] system call
    - 새로운 클라이언트가 리퀘스트를 날렸을 때(initiate)
    - 이미 존재하는 클라이언트가 리퀘스트를 날렸을 때
    -> return file descriptor etc..
    '''
    readable, writable, exceptional = select.select(
        inputs, outputs, inputs)
    for s in readable:
        if s is server:
            # accept
            connection, client_address = s.accept()
            print("accepted client")
            connection.setblocking(0)
            inputs.append(connection)
            '''important !!
            using "queue" - with each connection
            '''
            message_queues[connection] = queue.Queue()
        else: # not server
            data = s.recv(1024)
            print("from connected user: " + str(data))
            if data:
                data = input(' -> ')
                message_queues[s].put(data.encode())
                if s not in outputs:
                    outputs.append(s)
            else:
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]
    
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
            print(next_msg)
        except queue.Empty:
            outputs.remove(s)
        else:
            s.send(next_msg)

    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]