import serial
import quadcopter
import joystick
import asyncore

if __name__=='__main__':
	#s = serial.Serial('/dev/ttyUSB0', 38400)
	#quadcopter.make_serial_nonblocking(s)
	#q = quadcopter.Quadcopter(s)
	j = joystick.Joystick()
	j.open_path('/dev/input/js0')
	while True:
		asyncore.loop()

