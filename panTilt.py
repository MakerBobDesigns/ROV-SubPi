# Import the PCA9685 module.
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

pan = 4
tilt = 5
moveSpeed = 1
servoMin = 153  # Min pulse length out of 4096
center = 266
servoMax = 409  # Max pulse length out of 4096
panPos = center
tiltPos = center

pwm.set_pwm_freq(50)

def panTilt(control, input):
    if (control == 304) and (input == 1):
        pwm.set_pwm(pan, 0, center)
        pwm.set_pwm(tilt, 0, center)
        print ('Camera centered')
    elif control == 16:
        print ('control = 16')
        if input == 1:
            servoUp()
    return

def servoUp():
    print ('servoUp')
