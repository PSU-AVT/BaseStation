import asyncore

import afproto

def make_serial_nonblocking(s):
	s.nonblocking()
	s.setTimeout(0)
	s.setWriteTimeout(0)

class Quadcopter(asyncore.dispatcher):
	def __init__(self, quad_sock=None):
		asyncore.dispatcher.__init__(self)	
		self.set_quad_socket(quad_sock)
		self.out_buffer = ''
		self.in_buffer = ''
	
	def set_quad_socket(self, quad_sock):
		self.set_socket(quad_sock)
		self.connected = True
		self.quad_sock = quad_sock

	def readable(self):
		return self.connected

	def writable(self):
		return self.connected and len(self.out_buffer) > 0

	def handle_read(self):
		data = self.quad_sock.read()
		while data:
			self.in_buffer += data
			if len(self.in_buffer) > 3 and self.in_buffer[-1] == chr(afproto.end_byte) and self.in_buffer[-2] != chr(afproto.escape_byte):
				print 'extracting ',
				for ch in self.in_buffer:
					print '%x' % ord(ch),
				print
				payload, self.in_buffer = afproto.extract_payload(self.in_buffer)
				if payload:
					self.got_payload(payload)
			data = self.quad_sock.read()

	def got_payload(self, payload):
		print 'got payload %s' % payload

