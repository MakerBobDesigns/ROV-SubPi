from time import sleep

# Import the PCA9685 module.
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

pwm.set_pwm_freq(50)

pan = 4
tilt = 5
moveSpeed =1
servoMin = 123  # Min pulse length out of 4096
servoNeutral = 266
servoMax = 409  # Max pulse length out of 4096

def panTilt(panStatus, tiltStatus, centerStatus, panPos, tiltPos):
	if centerStatus == 1:
		panPos, tiltPos = servoCenter()
	else:
		if panStatus != 0:
			panPos = servoPan(panStatus, panPos)
		if tiltStatus != 0:
			tiltPos = servoTilt(tiltStatus, tiltPos)
	return panPos, tiltPos

def servoPan(panStatus, panPos):
	if (panStatus == 1) and (panPos < servoMax):
		panPos +=  moveSpeed
		pwm.set_pwm(pan, 0, panPos)
	elif (panStatus == -1) and (panPos > servoMin):
		panPos -= moveSpeed
		pwm.set_pwm(pan, 0, panPos)
	return panPos

def servoTilt(tiltStatus, tiltPos):
	if (tiltStatus == 1) and (tiltPos < servoMax):
		tiltPos +=  moveSpeed
		pwm.set_pwm(tilt, 0, tiltPos)
	elif (tiltStatus == -1) and (tiltPos > servoMin):
		tiltPos -= moveSpeed
		pwm.set_pwm(tilt, 0, tiltPos)
	return tiltPos

def servoCenter():
	panPos = tiltPos = servoNeutral
	for i in [pan, tilt]:
		pwm.set_pwm(i, 0, servoNeutral)
	return panPos, tiltPos

'''
servoCenter()
sleep(2)
panPos, tiltPos = panTilt(304, 1)
sleep(2)
'''
