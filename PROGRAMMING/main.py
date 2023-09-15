from microbit import *

#Continuous servo motor example:
#https://firialabs.com/blogs/lab-notes/continuous-rotation-servos-with-python-and-the-micro-bit

#servo motor values:
# 1.0 = 100% CW
# 1.1 = 80% CW
#...
# 1.5 = 0% STOPPED
# ...
# 1.9 = 80% CCW
# 2.0 = 100% CCW

#info on robot dims
#wheelDia = 37
#axleTrack = 90

#global variables

#driveTime=1450
#turnTime=700

class cont2Servo:
	def __init__(self, leftServoPin=pin1, compLServo=0.0, rightServoPin=pin2, compRServo=0.0):
		self.leftServo=leftServoPin
		self.rightServo=rightServoPin
		#20 ms = 50Hz RC Servo
		self.leftServo.set_analog_period(20)
		self.rightServo.set_analog_period(20)
		self.compL = compLServo
		self.compR = compRServo
		#self.stop()

	def set_ms_pulse(self, msLeft, msRight):
		self.leftServo.write_analog(1023 * msLeft / 20)
		self.rightServo.write_analog(1023 * msRight / 20)

	def stop(self):
		self.leftServo.write_analog(0)
		self.rightServo.write_analog(0)
		sleep(50)

	def forward(self):
		global driveTime
		#compensation is pos float number from 0 .0 to 0.5
		self.set_ms_pulse((2.0-self.compL), (1.0+self.compR))
		display.show(Image.ARROW_N)
		sleep(driveTime)
		self.stop()
		display.clear()

	def reverse(self):
		global driveTime
		self.set_ms_pulse((1.0+self.compL), (2.0-self.compR))
		display.show(Image.ARROW_S)
		sleep(driveTime)
		self.stop()
		display.clear()

	def leftTurn(self):
		global turnTime
		self.set_ms_pulse((1.0+self.compL), (1.0+self.compR))
		display.show(Image.ARROW_E)
		sleep(turnTime)
		self.stop()
		display.clear()

	def rightTurn(self):
		global turnTime
		self.set_ms_pulse((2.0-self.compL), (2.0-self.compR))
		display.show(Image.ARROW_W)
		sleep(turnTime)
		self.stop()
		display.clear()

#pi*axleTrack /4 = degree rotation -> timing next

#custom symbols for LED display
stopSign = Image("09990:" "77077:" "90009:" "77077:" "09990:")
checkSymbol = Image("0000:" "00009:" "00090:" "90900:" "09000:")

#setting menu variables for calibration
menu = 0

#setting up variables from values in text files
with open('comp1.py', 'r') as comp1:
	pin1Comp = float(comp1.read())
with open('comp2.py', 'r') as comp2:
	pin2Comp = float(comp2.read())
with open('driveTime.py', 'r') as dtime:
	driveTime = int(dtime.read())
with open('turnTime.py', 'r') as ttime:
    	turnTime = int(ttime.read())
with open('lang.py', 'r') as lang:
	language = int(lang.read())

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
enterButton = pin5

#pull up resistors on all pins
stopButton.set_pull(stopButton.PULL_UP)
playButton.set_pull(playButton.PULL_UP)
forwardButton.set_pull(forwardButton.PULL_UP)
reverseButton.set_pull(reverseButton.PULL_UP)
leftButton.set_pull(leftButton.PULL_UP)
rightButton.set_pull(rightButton.PULL_UP)
enterButton.set_pull(enterButton.PULL_UP)

#setting initial button states for comparison of pressing
buttonState1 = 0
lastState1 = 0
buttonState2 = 0
lastState2 = 0
buttonState3 = 0
lastState3 = 0
buttonState4 = 0
lastState4 = 0

robot1 = cont2Servo(compLServo=pin1Comp, compRServo=pin2Comp)

while True:

# read direction button states
	sleep(50)
#!!!need to condense into for loop for scanning!!
	buttonState1 = forwardButton.read_digital()
	buttonState2 = reverseButton.read_digital()
	buttonState3 = leftButton.read_digital()
	buttonState4 = rightButton.read_digital()
# pressing red button clears the program and stops the robot
	if stopButton.read_digital() == 0 and menu == 0:
		sleep(20)
		robot1.stop()
		sleep(1000)
		del recorded_button[:]
		display.show(checkSymbol)
		sleep(1000)
		display.clear()
		reset()
# pressing pins to record each movement
# !!!need to condense into IPO function!!!
	elif buttonState1 != lastState1:
		if buttonState1 == 0 and menu == 0:
			recorded_button.append(robot1.forward)
		sleep(50)
		lastState1 = buttonState1
	elif buttonState2 != lastState2:
		if buttonState2 == 0 and menu == 0:
			recorded_button.append(robot1.reverse)
		sleep(50)
		lastState2 = buttonState2
	elif buttonState3 != lastState3:
		if buttonState3 == 0 and menu == 0:
			recorded_button.append(robot1.leftTurn)
		sleep(50)
		lastState3 = buttonState3
	elif buttonState4 != lastState4:
		if buttonState4 == 0 and menu == 0:
			recorded_button.append(robot1.rightTurn)
		sleep(50)
		lastState4 = buttonState4
# start the recorded program
	elif playButton.read_digital() == 0 and menu == 0:
		sleep(20)
		if recorded_button != []:
			if language==1:
				display.scroll("Go")
			elif language==2:
				display.scroll("Ve")
			while i < len(recorded_button):
				recorded_button[i]()
				i = i + 1
			display.clear()
			del recorded_button[:]
			audio.play(Sound.TWINKLE)
			sleep(200)
			reset() #!!!need to address reset issue and count button presses vs. reset!!!
		else:
			if language==1:
				display.scroll("No Program")
			elif language==2:
				display.scroll("Sin programa")

#save current values and store them, exit menu
	if playButton.read_digital() == 0 and menu != 0:
		with open('comp1.py', 'w') as comp1:
			comp1.write(str(pin1Comp))
		with open('comp2.py', 'w') as comp2:
			comp2.write(str(pin2Comp))
		with open('driveTime.py', 'w') as dtime:
			dtime.write(str(driveTime))
		with open('turnTime.py', 'w') as ttime:
			ttime.write(str(turnTime))
		with open('lang.py', 'w') as lang:
			lang.write(str(language))
		if language==1:
			display.scroll("Store Values", delay=75)
		elif language==2:
			display.scroll("Almacenar valores", delay=75)
		sleep(100)
		menu = 0

# reset all values to defaults and store them, exit menu
	if stopButton.read_digital() == 0 and menu != 0:
		pin1Comp = 0.0
		pin2Comp = 0.0
		driveTime = 1450
		turnTime = 700
		language = 1
		sleep(50)
		with open('comp1.py', 'w') as comp1:
			comp1.write(str(pin1Comp))
		with open('comp2.py', 'w') as comp2:
			comp2.write(str(pin2Comp))
		with open('driveTime.py', 'w') as dtime:
			dtime.write(str(driveTime))
		with open('turnTime.py', 'w') as ttime:
			ttime.write(str(turnTime))
		with open('lang.py', 'w') as lang:
			lang.write(str(language))
		if language==1:
			display.scroll("Reset Values", delay=75)
		elif language==2:
			display.scroll("Restablecer valores", delay=75)
		sleep(100)
		menu = 0

#menu system thru enter button
	if enterButton.read_digital() == 0 and (menu == 0 or menu == 5):
		robot1.stop()
		if language==1:
			display.scroll("Motor Calibration", delay=75)
		elif language==2:
			display.scroll("Calibracion de motores", delay=75)
		sleep(100)
		menu = 1
	if enterButton.read_digital() == 0 and menu == 1:
		robot1.stop()
		if language==1:
			display.scroll("Distance Calibration", delay=75)
		elif language==2:
			display.scroll("Calibracion de distancia", delay=75)
		sleep(100)
		menu = 2
	if enterButton.read_digital() == 0 and menu == 2:
		robot1.stop()
		if language==1:
			display.scroll("Turning Calibration", delay=75)
		elif language==2:
			display.scroll("Calibracion de giro", delay=75)
		sleep(100)
		menu = 3
	if enterButton.read_digital() == 0 and menu == 3:
		robot1.stop()
		if language==1:
			display.scroll("Testing...", delay=75)
		elif language==2:
			display.scroll("Pruebas...", delay=75)
		sleep(100)
		menu = 4
	if enterButton.read_digital() == 0 and menu == 4:
		robot1.stop()
		if language==1:
			display.scroll("Language - Idioma", delay=75)
		elif language==2:
			display.scroll("Idioma - Language", delay=75)
		sleep(100)
		menu = 5

#calibration menu #5 for language
	if forwardButton.read_digital() == 0 and menu == 5:
		display.scroll("ENGLISH", delay = 75)
		language = 1
		sleep(100)
	if reverseButton.read_digital() == 0 and menu == 5:
		display.scroll("ESPANOL", delay = 75)
		language = 2
		sleep(100)

#calibration menu #4 testing the settings
	if forwardButton.read_digital() == 0 and menu == 4:
		if language==1:
			display.scroll("Forward 2X", delay=75)
		elif language==2:
			display.scroll("Adelante 2X", delay=75)
		sleep(1000)
		robot1.forward()
		sleep(driveTime)
		robot1.forward()
		sleep(driveTime)
		if language==1:
			display.scroll("Testing...", delay=75)
		elif language==2:
			display.scroll("Pruebas...", delay=75)
	if reverseButton.read_digital() == 0 and menu == 4:
		if language==1:
			display.scroll("Reverse 2X", delay=75)
		elif language==2:
			display.scroll("Inverso 2X", delay=75)
		sleep(1000)
		robot1.reverse()
		sleep(driveTime)
		robot1.reverse()
		sleep(driveTime)
		if language==1:
			display.scroll("Testing...", delay=75)
		elif language==2:
			display.scroll("Pruebas...", delay=75)
	if leftButton.read_digital() == 0 and menu == 4:
		if language==1:
			display.scroll("Left Turn", delay=75)
		elif language==2:
			display.scroll("Giro a la izquierda", delay=75)
		sleep(1000)
		robot1.leftTurn()
		sleep(turnTime)
		robot1.rightTurn()
		sleep(turnTime)
		if language==1:
			display.scroll("Testing...", delay=75)
		elif language==2:
			display.scroll("Pruebas...", delay=75)
	if rightButton.read_digital() == 0 and menu == 4:
		if language==1:
			display.scroll("Right Turn", delay=75)
		elif language==2:
			display.scroll("Vuelta a la derecha", delay=75)
		sleep(1000)
		robot1.rightTurn()
		sleep(turnTime)
		robot1.leftTurn()
		sleep(turnTime)
		if language==1:
			display.scroll("Testing...", delay=75)
		elif language==2:
			display.scroll("Pruebas...", delay=75)

#calibration menu #3 turning time
	if forwardButton.read_digital() == 0 and menu == 3:
		turnTime=turnTime+10
		display.scroll(turnTime, delay=75)
		sleep(100)
	if reverseButton.read_digital() == 0 and menu == 3:
		if turnTime > 9:
			turnTime=turnTime-10
			display.scroll(turnTime, delay=75)
			sleep(100)
		else:
			if language==1:
				display.scroll("Zero", delay=75)
			elif language==2:
				display.scroll("Cero", delay=75)

#calibration menu #2 distance set time
	if forwardButton.read_digital() == 0 and menu == 2:
		driveTime=driveTime+50
		display.scroll(driveTime, delay=75)
		sleep(100)
	if reverseButton.read_digital() == 0 and menu == 2:
		if driveTime > 49:
			driveTime=driveTime-50
			display.scroll(driveTime, delay=75)
			sleep(100)
		else:
			if language==1:
				display.scroll("Zero", delay=75)
			elif language==2:
				display.scroll("Cero", delay=75)

#calibration menu #1 left right servo balance compensation
	if rightButton.read_digital() == 0 and menu == 1:
		if pin2Comp < .5:
			pin2Comp=pin2Comp+.01
			comp2Display=int(100-(pin2Comp*200))
			display.scroll("%s%%"%comp2Display, delay=75)
			sleep(100)
		else:
			if language==1:
				display.scroll("Maximum", delay=75)
			elif language==2:
				display.scroll("Maximo", delay=75)
	if leftButton.read_digital() == 0 and menu == 1:
		if pin1Comp < .5:
			pin1Comp=pin1Comp+.01
			comp1Display=int(100-(pin1Comp*200))
			display.scroll("%s%%"%comp1Display, delay=75)
			sleep(100)
		else:
			if language==1:
				display.scroll("Maximum", delay=75)
			elif language==2:
				display.scroll("Maximo", delay=75)
