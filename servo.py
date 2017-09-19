import sys
sys.path.append('/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_PWM_Servo_Driver/')

from Adafruit_PWM_Servo_Driver import PWM
from evdev import InputDevice, categorize, ecodes, KeyEvent
import time

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)
gamepad = InputDevice('/dev/input/event0')

servoMin = 153  # Min pulse length out of 4096
servoStop = 266
servoChannel = 4
servoMax = 409  # Max pulse length out of 4096
pwm.setPWMFreq(50)

for event in gamepad.read_loop():
    if event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RY$
                servoPos = absevent.event.value/256 + 281
                pwm.setPWM(servoChannel, 0, servoPos)
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        #print ecodes.bytype[keyevent.event.type][keyevent.event.code], keyev$
        #print (keyevent)
        if keyevent.keycode[0] == 'BTN_A' and keyevent.keystate == KeyEvent.k$
                pwm.setPWM(servoChannel, 0, servoMin)
        if keyevent.keycode[0] == 'BTN_B' and keyevent.keystate == KeyEvent.k$
                pwm.setPWM(servoChannel, 0, servoMax)

while (True):
  # Change speed of continuous servo on channel O
  pwm.setPWM(servoChannel, 0, servoMin)
  time.sleep(1)
  pwm.setPWM(servoChannel, 0, servoStop)
  time.sleep(1)
  pwm.setPWM(servoChannel, 0, servoMax)
  time.sleep(1)
