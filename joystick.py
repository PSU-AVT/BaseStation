import os
import asyncore
import struct

class JoystickEvent(object):
	def __init__(self, time, value, event_type, number):
		self.time = time
		self.value = value
		self.event_type = event_type
		self.number = number

class Joystick(asyncore.dispatcher):
	def __init__(self, path=None):
		asyncore.dispatcher(self)
		if path != None:
			self.open(path)

	def open(self, path):
		self.fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
		self.set_socket(self.fd)
		self.connected = True

	def readable(self):
		return True

	def writable(self):
		return False

	def handle_read(self):
		data = os.read(self.fd, 8)
		event = JoystickEvent(*struct.unpack('IhBB', data))
		self.handle_event(event)

	def handle_event(self, event):
		pass

if __name__=='__main__':
	pass

