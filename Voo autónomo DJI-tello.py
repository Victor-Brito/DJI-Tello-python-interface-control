

import threading 
import socket
import sys
import time
import platform  

host = ''
port = 9000
locaddr = (host,port) 


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tello_address = ('192.168.10.1', 8889)

sock.bind(locaddr)

def recv():
    count = 0
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break


print ('\r\n\r\nTello Python3 Demo.\r\n')

print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

print ('end -- quit demo.\r\n')


#recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()

while True: 
    try:
        python_version = str(platform.python_version())
        version_init_num = int(python_version.partition('.')[0]) 
       # print (version_init_num)
        if version_init_num == 3:
            msg = input("");
        elif version_init_num == 2:
            msg = raw_input("");
        
        if not msg:
            break  

        if 'end' in msg:
            print ('...')
            sock.close()  
            break

        if '4x4' in msg:
            #=================|
            # Voar no quadrado|
            #=================|
            msg = 'command'
            msg = msg.encode(encoding="utf-8") 
            sent = sock.sendto(msg, tello_address)
            print('Iniciando rota de voo')
            time.sleep(1)

            
            # Decolar
            print ('Decolando')
            msg = 'takeoff'
            msg = msg.encode(encoding="utf-8") 
            sent = sock.sendto(msg, tello_address)
            time.sleep(5)

            
            #Ir para frente de acordo com os cm
            print('indo 60 cm para frente')
            msg = 'forward 60'
            msg = msg.encode(encoding="utf-8") 
            sent = sock.sendto(msg, tello_address)
            time.sleep(5)

            #Girar 90º em seu eixo para direita
            print('girar 90º')
            msg = 'cw 90'
            msg = msg.encode(encoding="utf-8") 
            sent = sock.sendto(msg, tello_address)
            time.sleep(5)

            #Ir para frente de acordo com os cm
            print('indo 60 cm para frente')
            msg = 'forward 60'
            msg = msg.encode(encoding="utf-8") 
            sent = sock.sendto(msg, tello_address)
            time.sleep(5)

            #Girar 90º em seu eixo para direita
            print('girar 90º')
            msg = 'cw 90'
            msg = msg.encode(encoding="utf-8") 
            sent = sock.sendto(msg, tello_address)
            time.sleep(5)

            #Ir para frente de acordo com os cm
            print('indo 60 cm para frente')
            msg = 'forward 60'
            msg = msg.encode(encoding="utf-8") 
            sent = sock.sendto(msg, tello_address)
            time.sleep(5)
            
            # Descer
            print('Descendo')
            msg = 'land'
            msg = msg.encode(encoding="utf-8") 
            sent = sock.sendto(msg, tello_address)
            time.sleep(3)
            print ('Finalizado')

            

        
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()  
        break




