from tkinter import*
import threading 
import socket
import sys
import time
import platform  
import cv2
import os
import tellopy
import av
import numpy

#Configs do Tello
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

#--------Comandos-------------------

def encode(frame, ovstream, output):
    """
    convert frames to packets and write to file
    """
    try:
        pkt = ovstream.encode(frame)
    except Exception as err:
        print("encoding failed{0}".format(err))

    if pkt is not None:
        try:
            output.mux(pkt)
        except Exception:
            print('mux failed: ' + str(pkt))
    return True

def main():
    # Set up tello streaming
    drone = tellopy.Tello()
    drone.log.set_level(2)
    drone.connect()
    drone.start_video()

    # container for processing the packets into frames
    container = av.open(drone.get_video_stream())
    video_st = container.streams.video[0]

    # stream and outputfile for video
    output = av.open('archive.mp4', 'w')
    ovstream = output.add_stream('mpeg4', video_st.rate)
    ovstream.pix_fmt = 'yuv420p'
    ovstream.width = video_st.width
    ovstream.height = video_st.height

    counter = 0
    save = True
    for packet in container.demux((video_st,)):
        for frame in packet.decode():
            # convert frame to cv2 image and show
            image = cv2.cvtColor(numpy.array(
                frame.to_image()), cv2.COLOR_RGB2BGR)
            cv2.imshow('frame', image)
            key = cv2.waitKey(1) & 0xFF


def Emergencia():
    msg = 'emergency'
    msg = msg.encode(encoding="utf-8") 
    sent = sock.sendto(msg, tello_address)


def decolar():
    msg = 'command'
    msg = msg.encode(encoding="utf-8") 
    sent = sock.sendto(msg, tello_address)

    time.sleep(1)

    msg = 'takeoff'
    msg = msg.encode(encoding="utf-8") 
    sent = sock.sendto(msg, tello_address)
    

def pousar():
    msg = 'land'
    msg = msg.encode(encoding="utf-8") 
    sent = sock.sendto(msg, tello_address)
    
def Bateria():
    msg = 'battery?'
    msg = msg.encode(encoding="utf-8") 
    sent = sock.sendto(msg, tello_address)


def Subir():
    msg = 'up 20'
    msg = msg.encode(encoding="utf-8") 
    sent = sock.sendto(msg, tello_address)

def Descer():
    msg = 'down 20'
    msg = msg.encode(encoding="utf-8") 
    sent = sock.sendto(msg, tello_address)

def GirarDireita():
    msg = 'cw 20'
    msg = msg.encode(encoding="utf-8") 
    sent = sock.sendto(msg, tello_address)

def GirarEsquerda():
    msg = 'ccw 20'
    msg = msg.encode(encoding="utf-8") 
    sent = sock.sendto(msg, tello_address)

def Frente():
    msg = 'forward 40'
    msg = msg.encode(encoding="utf-8") 
    sent = sock.sendto(msg, tello_address)

def Tras():
    msg = 'back 40'
    msg = msg.encode(encoding="utf-8") 
    sent = sock.sendto(msg, tello_address)

def EsquerdaInclinação():
    msg = 'left 40'
    msg = msg.encode(encoding="utf-8") 
    sent = sock.sendto(msg, tello_address)

def DireitaInclinação():
    msg = 'right 40'
    msg = msg.encode(encoding="utf-8") 
    sent = sock.sendto(msg, tello_address)


#---------- MAIN FRAME ----------
def on_closing():
    root.destroy()
    os._exit(1)





root = Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.geometry('600x600+200+200')
root.wm_title("DJI Tello")

#---------- COMMANDS FRAME ----------
commandsFrame = LabelFrame(root, text="Comandos")
commandsFrame.place(rely=0, relx=0, relwidth=1, relheight=0.7)



btn_connect_cam = Button(commandsFrame, text="cam")
btn_connect_cam.place(relx=0.45, relwidth=0.2, relheight=0.1, rely=0.2)

btn_connect_cam = Button(commandsFrame, text="Bateria", command=Bateria)
btn_connect_cam.place(relx=0.25, relwidth=0.2, relheight=0.1, rely=0.2)

label_status_con = Label(commandsFrame, text="Desconectado", fg="red", font=("Helvetica", 12))
label_status_con.place(rely=0.1, relwidth=0.2, relheight=0.1, relx=0.7)

btn_takeoff = Button(commandsFrame, text="Decolar", command=decolar)
btn_takeoff.place(relx=0.05, relwidth=0.2, relheight=0.1, rely=0.3)

btn_land = Button(commandsFrame, text="Pousar", command=pousar)
btn_land.place(relx=0.25, relwidth=0.2, relheight=0.1, rely=0.3)

btn_emergency = Button(commandsFrame, text="Emergencia", command=Emergencia)
btn_emergency.place(relx=0.45, relwidth=0.2, relheight=0.1, rely=0.3)

label_status_aircraft = Label(commandsFrame, text="Desconectado", fg="red", font=("Helvetica", 12))
label_status_aircraft.place(rely=0.3, relwidth=0.2, relheight=0.1, relx=0.7)

#------------------ ROTATION -----------------

btn_move_up = Button(commandsFrame, text="Subir", command=Subir)
btn_move_up.place(relx=0.15, relwidth=0.2, relheight=0.1, rely=0.5)

btn_move_cw = Button(commandsFrame, text="Girar", command=GirarEsquerda)
btn_move_cw.place(relx=0.05, relwidth=0.2, relheight=0.1, rely=0.6)

btn_move_down = Button(commandsFrame, text="Descer", command=Descer)
btn_move_down.place(relx=0.15, relwidth=0.2, relheight=0.1, rely=0.7)

btn_move_ccw = Button(commandsFrame, text="Girar", command=GirarDireita)
btn_move_ccw.place(relx=0.25, relwidth=0.2, relheight=0.1, rely=0.6)

#----------------------- MOVEMENT -------------------

btn_move_up = Button(commandsFrame, text="Frente", command=Frente)
btn_move_up.place(relx=0.65, relwidth=0.2, relheight=0.1, rely=0.5)

btn_move_cc = Button(commandsFrame, text="Esquerda", command=EsquerdaInclinação)
btn_move_cc.place(relx=0.55, relwidth=0.2, relheight=0.1, rely=0.6)

btn_move_down = Button(commandsFrame, text="Tras", command=Tras)
btn_move_down.place(relx=0.65, relwidth=0.2, relheight=0.1, rely=0.7)

btn_move_cc = Button(commandsFrame, text="Direita", command=DireitaInclinação)
btn_move_cc.place(relx=0.75, relwidth=0.2, relheight=0.1, rely=0.6)

# ------------------------- Voo automático
label_flips = Label(commandsFrame, text="Flips", font=("Helvetica", 12))
label_flips.place(rely=0.8, relwidth=0.2, relheight=0.1, relx=0.05)

btn_flip_front = Button(commandsFrame, text="Voo automático")
btn_flip_front.place(relx=0.05, relwidth=0.2, relheight=0.1, rely=0.9)


#---------- TERMINAL FRAME ----------
terminalFrame = LabelFrame(root, text="Terminal")
terminalFrame.place(rely=0.7, relx=0, relwidth=1, relheight=0.3)

terminalList = Listbox(terminalFrame)
terminalList.pack(fill="both", expand=1)

#---------- START APP ----------
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

        # Send data
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()  

        root.mainloop()

        break




