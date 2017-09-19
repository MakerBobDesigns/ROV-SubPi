from ROVServer import setupServer, setupConnection
from panTilt import panTilt

def dataTransfer(conn):
    # A big loop that sends/receives data until told not to.
    while True:
        # Receive the data
        data = conn.recv(16) # receive the data
        # Split the data such that you separate the command
        # from the rest of the data.
        dataMessage = data.split(' ', 1)
        control = int(dataMessage[0])
        input = int(dataMessage[1])
        if control in [0, 1, 3, 4]:
            reply = "Joystick"
            print (reply)
            #Call speedControl (control, input) 
            #break
        elif control in [2, 5, 310, 311]:
            reply = "Manipulator"
            print (reply)
            #Call manipulator (control, input)
            #break
        elif control in [16, 17, 304]:
            reply = "Pan / Tilt"
            print(reply)
            panTilt(control, input)
            #break
        elif control == 305:
            if position == 1:
                reply = "Lights"
                print (reply)
                #Call lights()
                #break
            else:
                break
        elif control in [307, 308]:
            reply = "Ballast"
            print (reply)
            #Call ballast (control, input)
            #break
        elif control == 'EXIT':
            print("Our client has left us :(")
            break
        elif control == 'KILL':
            print("Our server is shutting down.")
            s.close()
            break
        else:
            reply = 'Unknown Command'
            print (reply)
            #break
        # Send the reply back to the client
        conn.send(reply)
        print("Data has been sent!")
        break
    conn.close()

s = setupServer()

while True:
    try:
        conn = setupConnection(s)
        dataTransfer(conn)
    except:
        break


