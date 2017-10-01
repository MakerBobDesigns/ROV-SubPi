from ROVServer import setupServer, setupConnection
from time import sleep
import threading

# Import the PCA9685 module.
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

pwm.set_pwm_freq(50)

panChannel = 4
tiltChannel = 5
moveSpeed =1 # The speed that the camera moves while button held
servoMin = 123  # Min/Max/Center for small pan/tilt servos
servoNeutral = 266
servoMax = 409 
panPos = tiltPos = servoNeutral # Camera centered intitially
panning = tilting = False

controlCodes = ("0", "1", "2", "3", "4", "5", "16", "17",
		"304", "305", "307", "308", "310", "311",
		"314", "315", "316", "317", "318")
status = [128, -129, 0, 128, -129, 0, 0, 0,
	  0, 0, 0, 0, 0, 0,
	  0, 0, 0, 0, 0]

def panTilt(centerStatus):
	global panStatus, panPos, panning, tiltStatus, tiltPos, tilting
	if (centerStatus == 1) and not (panning or tilting):
		servoCenter()
	else:
		if (panStatus != 0) and not panning:
			panThread = threading.Thread(target=servoPan)
			panning = True
			panThread.start()
		if (tiltStatus != 0) and not tilting:
			tiltThread = threading.Thread(target=servoTilt)
                        tilting = True
                        tiltThread.start()

def servoPan():
	global panStatus, panPos, panning
	print ('panning thread')
	while panStatus != 0:
		while (panStatus == 1) and (panPos <= servoMax):
			panPos +=  moveSpeed
			pwm.set_pwm(panChannel, 0, panPos)
		while (panStatus == -1) and (panPos >= servoMin):
			panPos -= moveSpeed
			pwm.set_pwm(panChannel, 0, panPos)
	panning = False

def servoTilt():
	global tiltStatus, tiltPos, tilting
        print ('tilting thread')
        while tiltStatus != 0:
                while (tiltStatus == 1) and (tiltPos <= servoMax):
                        tiltPos +=  moveSpeed
                        pwm.set_pwm(tiltChannel, 0, tiltPos)
                while (tiltStatus == -1) and (tiltPos >= servoMin):
                        tiltPos -= moveSpeed
                        pwm.set_pwm(tiltChannel, 0, tiltPos)
        tilting = False

def servoCenter():
	global panPos, tiltPos
	panPos = tiltPos = servoNeutral
	for i in [panChannel, tiltChannel]:
		pwm.set_pwm(i, 0, servoNeutral)

def dataTransfer(conn):
	#storedVal = [266, 266, 0]
	global panStatus, tiltStatus, LEDStatus, panPos, tiltPos
	# loop that sends/receives data until told not to.
	while True:
		data = conn.recv(16) # receive the data
		# Split the data such that you separate the command
		# from the rest of the data.
		dataMessage = data.split(' ', 1)
		control = dataMessage[0]
		newStatus = int(dataMessage[1])
		status[controlCodes.index(control)] = newStatus
		panStatus = status[6]
		tiltStatus = status[7]
		reply = "Status Updated"
		# Send the reply back to the client
		conn.send(reply)

		#control in [16, 17, 304]:
		panTilt(status[8])
	
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

s = setupServer()

while True:
    try:
        conn = setupConnection(s)
        dataTransfer(conn)
    except:
        break


