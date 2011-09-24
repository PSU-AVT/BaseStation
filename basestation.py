import serial
import quadcopter

if __name__=='__main__':
	s = serial.Serial('/dev/ttyUSB0')
	quadcopter.make_serial_nonblocking(s)
	q = quadcopter.Quadcopter(s)
	while True:
		asyncore.loop()

