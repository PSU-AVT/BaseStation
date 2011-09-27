import serial
import quadcopter
import struct
import joystick
import asyncore

class QuadJoystick(joystick.Joystick):
	def __init__(self, quadcopter):
		joystick.Joystick.__init__(self)
		self.quadcopter = quadcopter
		self.event_axis_handlers = {
			0: self.handle_axis_roll,
			1: self.handle_axis_pitch,
			2: self.handle_axis_vertical }

	def handle_event(self, event):
		print 'event %d %d' % (event.number, event.value)
		try:
			self.event_axis_handlers[event.number](event)
		except KeyError:
			pass

	def handle_axis_roll(self, event):
		out = struct.pack('BB', 1, (event.value/2**8)%255)
		self.quadcopter.send_payload(out)

	def handle_axis_pitch(self, event):
		out = struct.pack('BB', 2, (event.value/2**8)%255)
		self.quadcopter.send_payload(out)

	def handle_axis_vertical(self, event):
		out = struct.pack('BB', 3, ((-1*event.value) + 32768)>>8)
		self.quadcopter.send_payload(out)

if __name__=='__main__':
	s = serial.Serial('/dev/ttyUSB0', 38400, 8)
	quadcopter.make_serial_nonblocking(s)
	q = quadcopter.Quadcopter(s)
	j = QuadJoystick(q)
	j.open_path('/dev/input/js0')
	q.send_payload('\x04')
	while True:
		asyncore.loop()

