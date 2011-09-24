import asyncore

import afproto

def make_serial_nonblocking(self, s):
	s.nonblocking()
	s.setTimeout(0)
	s.setWriteTimeout(0)

class Quadcopter(asyncore.dispatcher):
	def __init__(self, quad_sock=None):
		asyncore.dispatcher.__init(self)	
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
		return self.connected and len(out_buffer) > 0

	def handle_read(self):
		data = self.quad_sock.read()
		while data:
			buff += data
			if len(buff) > 3 and buff[-1] == afproto.end_byte and buff[-2] != afproto.escape_byte:
				payload, buff = afproto.extract_payload(buff)
				if payload:
					self.got_payload(payload)
			data = self.quad_sock.read()

	def got_payload(self, payload):
		pass

