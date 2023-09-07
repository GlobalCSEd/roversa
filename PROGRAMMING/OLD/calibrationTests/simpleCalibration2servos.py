from microbit import *
import time
import machine

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

#much simpler implementation of rotation - create lib:
#https://firialabs.com/blogs/lab-notes/continuous-rotation-servos-with-python-and-the-micro-bit

#pin1=left
#pin2=right
menu = 0
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

# 50Hz to 20 ms pulse
pin1.set_analog_period(20)
pin2.set_analog_period(20)

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

with open('comp1.txt', 'r') as comp1:
	pin1Comp = float(comp1.read())
with open('comp2.txt', 'r') as comp2:
	pin2Comp = float(comp2.read())

while True:
	if pin5.read_digital() == 0:
		menu = 0
		with open('comp1.txt', 'w') as comp1:
			comp1.write(str(pin1Comp))
		with open('comp2.txt', 'w') as comp2:
			comp2.write(str(pin2Comp))
		display.scroll("Storing Values", delay=75)
	if pin8.read_digital() == 0 and menu == 0:
		stop()
		display.scroll("Cal", delay = 75)
		sleep(100)
		menu = 1
	if pin15.read_digital() == 0 and menu == 1:
		if pin2Comp < .5:
			pin2Comp=pin2Comp+.01
			comp2Display=int(100-(pin2Comp*200))
			display.scroll("%s%%"%comp2Display, delay=75)
			sleep(100)
		else:
			display.scroll("MAX")
	if pin16.read_digital() == 0 and menu == 1:
		if pin1Comp < .5:
			pin1Comp=pin1Comp+.01
			comp1Display=int(100-(pin1Comp*200))
			display.scroll("%s%%"%comp1Display, delay=75)
			sleep(100)
		else:
			display.scroll("MAX")
	if pin13.read_digital() == 0 and menu == 0:
		forward()
	if pin9.read_digital() == 0 and menu == 0:
		pin1Comp = 0.0
		pin2Comp = 0.0
		display.scroll("Reset Values", delay=75)






