from microbit import *
import time
import machine

#much simpler implementation of rotation - create lib:
#https://firialabs.com/blogs/lab-notes/continuous-rotation-servos-with-python-and-the-micro-bit

#pin1=left
#pin2=right

#controlling distance with time
forwardreverseTime = 1450
turnTime = 700
#servo motor compensation: 
# 1.0 = 100% C 
# 1.1 = 80% C
#...
# 1.5 = 0% STOPPED
# ...
# 1.9 = 80% CC
# 2.0 = 100% CC
pin1Comp = 0.0
pin2Comp = 0.125
# 50Hz to 20 ms pulse
pin1.set_analog_period(20)
pin2.set_analog_period(20)

#rotationSquare = 0.769148546224 #35.5*pi/145 = rev  |  35.5mm wheel dia, 145mm distance of mat

#specific motor control functions
def stop():
	pin1.write_analog(0)
	pin2.write_analog(0)
	#display.show(stopSign)
	sleep(1000)

def forward():
	pin1.write_analog(1023 * (2.0-pin1Comp) / 20)
	pin2.write_analog(1023 * (1.0+pin2Comp) / 20)	
	#display.show(Image.ARROW_N)
	sleep(forwardreverseTime) #one tire revolution
	stop()

def leftTurn():
	pin1.write_analog(1023 * (1.0+pin1Comp) / 20)
	pin2.write_analog(1023 * (1.0+pin2Comp) / 20)
	#display.show(Image.ARROW_W)
	sleep(turnTime) #90 deg turn
	stop()

def rightTurn():
	pin1.write_analog(1023 * (2.0-pin1Comp) / 20)
	pin2.write_analog(1023 * (2.0-pin2Comp) / 20)
	#display.show(Image.ARROW_E)
	sleep(turnTime)
	stop()

def reverse():
	pin1.write_analog(1023 * (1.0+pin1Comp) / 20)
	pin2.write_analog(1023 * (2.0-pin2Comp) / 20)	
	#motors1.set_motors_speed(-motorcompL,-motorcompR)
	#display.show(Image.ARROW_S)
	sleep(forwardreverseTime)
	stop()

#custom symbols for LED display
stopSign = Image("09990:" "77077:" "90009:" "77077:" "09990:")
checkSymbol = Image("0000:" "00009:" "00090:" "90900:" "09000:")

#array to store directions when entered
recorded_button = []
i = 0
#pin assignments not interacting with MB buttons, i2c, or LED array on V2
stopButton = pin9
playButton = pin8
forwardButton = pin13
reverseButton = pin14
leftButton = pin16
rightButton = pin15

#pull up resistors on all pins
stopButton.set_pull(stopButton.PULL_UP)
playButton.set_pull(playButton.PULL_UP)
forwardButton.set_pull(forwardButton.PULL_UP)
reverseButton.set_pull(reverseButton.PULL_UP)
leftButton.set_pull(leftButton.PULL_UP)
rightButton.set_pull(rightButton.PULL_UP)

#setting initial button states for comparison of pressing
buttonState1 = 0
lastState1 = 0
buttonState2 = 0
lastState2 = 0
buttonState3 = 0
lastState3 = 0
buttonState4 = 0
lastState4 = 0

while True:
# read direction button states
	sleep(50)
#!!!need to condense into for loop for scanning!!
	buttonState1 = forwardButton.read_digital()
	buttonState2 = reverseButton.read_digital()
	buttonState3 = leftButton.read_digital()
	buttonState4 = rightButton.read_digital()
# pressing red button clears the program and stops the robot
	if stopButton.read_digital() == 0:
		sleep(20)
		stop()
		sleep(1000)		
		del recorded_button[:]
		display.show(checkSymbol)
		sleep(1000)
		display.clear()
		reset()
# pressing pins to record each movement
# !!!need to condense into IPO function!!!
	elif buttonState1 != lastState1:
		if buttonState1 == 0:
			recorded_button.append(forward)
		sleep(50)
		lastState1 = buttonState1
	elif buttonState2 != lastState2:
		if buttonState2 == 0:
			recorded_button.append(reverse)
		sleep(50)
		lastState2 = buttonState2
	elif buttonState3 != lastState3:
		if buttonState3 == 0:
			recorded_button.append(leftTurn)
		sleep(50)
		lastState3 = buttonState3
	elif buttonState4 != lastState4:
		if buttonState4 == 0:
			recorded_button.append(rightTurn)
		sleep(50)
		lastState4 = buttonState4
# start the recorded program
	elif playButton.read_digital() == 0:
		sleep(20)
		if recorded_button != []:
			display.scroll("GO!")
			while i < len(recorded_button):
				recorded_button[i]()
				i = i + 1			
			display.clear()
			del recorded_button[:]
			audio.play(Sound.TWINKLE)
			sleep(2000)
			reset() #!!!need to address reset issue and count button presses vs. reset!!!
		else:
			display.scroll("No program!")