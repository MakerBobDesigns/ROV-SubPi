from ROVServer import setupServer, setupConnection
from panTilt import panTilt

controlCodes = ("0", "1", "2", "3", "4", "5", "16", "17",
		"304", "305", "307", "308", "310", "311",
		"314", "315", "316", "317", "318")
status = [128, -129, 0, 128, -129, 0, 0, 0,
	  0, 0, 0, 0, 0, 0,
	  0, 0, 0, 0, 0]

def dataTransfer(conn):
	storedVal = [266, 266, 0]
	# loop that sends/receives data until told not to.
	while True:
		data = conn.recv(16) # receive the data
		# Split the data such that you separate the command
		# from the rest of the data.
		dataMessage = data.split(' ', 1)
		control = dataMessage[0]
		newStatus = int(dataMessage[1])
		status[controlCodes.index(control)] = newStatus
		reply = "Status Updated"
		# Send the reply back to the client
		conn.send(reply)
		storedVal = statusUpdate(status, storedVal)
	
def statusUpdate(status, storedVal):
	panPos = storedVal[0]
	tiltPos = storedVal[1]
	onOff = storedVal[2]

	#control in [16, 17, 304]:
	panPos, tiltPos = panTilt(status[6], status[7], status[8], panPos, tiltPos)

	#control in [0, 1, 3, 4]:
	#Call speedControl (status[0], status[1], status[3], status[4]) 
        
	#control in [2, 5, 310, 311]:
	#Call manipulator (status[2], status[5], status[12], status[13])
        
	#control == 305:
	#Call onOff = lights(status[9], onOff)
	
	#control in [307, 308]:
	#Call ballast (status[10], status[11])
	
	#Unassigned buttons:
	#317, 318 Joysticks
	#314, 315, 316 

	return (panPos, tiltPos, onOff)

s = setupServer()

while True:
    try:
        conn = setupConnection(s)
        dataTransfer(conn)
    except:
        break


