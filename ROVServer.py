import socket

host = '10.66.66.2'
port = 2222

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete.")
    return s

def dataTransfer(conn):
    # A big loop that sends/receives data until told not to.
    while True:
        # Receive the data
        data = conn.recv(1024) # receive the data
        # ''''''' data = data.decode('utf-8')
        # Split the data such that you separate the command
        # from the rest of the data.
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]
        command = int(command)
        if command > 100:
            reply = "Button"
            print (reply)
            #break
        elif command <100:
            reply = "Analog"
            print (reply)
            #break
        elif command == 'PANTILT':
            print("Move pan / tilt camera")
            storeFile(dataMessage[1])
            print("FINISHED STORING FILE")
            break
        elif command == 'LED_ON':
            callLED()
            reply = 'LED was on'
        elif command == 'EXIT':
            print("Our client has left us :(")
            break
        elif command == 'KILL':
            print("Our server is shutting down.")
            s.close()
            break
        else:
            reply = 'Unknown Command'
            break
        # Send the reply back to the client
        conn.send(reply)
        #conn.sendall(str.encode(reply))
        print("Data has been sent!")
        break
    conn.close()

def setupConnection():
    s.listen(1) # Allows one connection at a time.
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn

s = setupServer()

while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)
    except:
        break


