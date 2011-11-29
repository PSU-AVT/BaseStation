import time
import struct
import settings

from PyQt4 import QtCore, QtGui, QtNetwork

class UdpClient(QtNetwork.QUdpSocket):
	def __init__(self):
		super(UdpClient, self).__init__()
	
	def setDestination(self, hostname, port):
		self.hostname = hostname
		self.bind()
		self.connectToHost(hostname, port)

	def sendData(self, data):
		if self.isValid():
			sent = self.write(data)
			if sent == -1:
				print 'Error code ', self.error()

class ControlGw(UdpClient):
	command_id = settings.ControlGw.command_id
	response_id = settings.ControlGw.response_id

	def __init__(self):
		super(ControlGw, self).__init__()

	def sendCommand(self, command_id, data):
		msg = struct.pack('B', command_id)
		msg += data
		self.sendData(msg)

class StatePublisher(UdpClient):
	def __init__(self):
		super(StatePublisher, self).__init__()
		self.subscriptions = []
		self.resub_timer = QtCore.QTimer(self)
		self.resub_timer.setInterval(500)
		self.resub_timer.setSingleShot(False)
		self.resub_timer.timeout.connect(self.resub_timeout)
		self.resub_timer.start()

	def subscribeTo(prefix, persistent=True):
		if persistent:
			self.subscriptions.append(prefix)
		self.sendData(prefix)

	def resub_timeout(self):
		data = ''
		for sub in self.subscriptions:
			data += sub + '\n'
		# remove trailing \n
		data = data[:-1]
		if len(data) > 0:
			self.sendData(data)

class ConnectionManager(QtCore.QObject):
	def __init__(self):
		super(ConnectionManager, self).__init__()

		self.controlgw_handlers = {
			ControlGw.response_id['Pong']: self.handle_cgw_pong
		}

		self.timeout_secs = 10
		self.is_connected = False

	def connected(self):
		return self.is_connected

	def do_connect(self, host):
		self.is_connected = True
		self.progress = QtGui.QProgressDialog("Connecting to quadcopter...", "Cancel", 0, 2)
		self.progress.canceled.connect(self.do_disconnect)
		self.progress.setVisible(True)
		self.progress.setValue(0)

		self.control_sock = ControlGw()
		self.control_sock.setDestination(host, 8091)
		self.control_sock.connected.connect(self.handle_cgw_connected)
		self.control_sock.readyRead.connect(self.got_controlgw_data)

		self.state_sock = StatePublisher()
		self.state_sock.setDestination(host, 8092)

		# We dont have a verify state connection method
		self.progress.setValue(1 + self.progress.value())
		self.handle_progress_updated()

	def do_disconnect(self):
		if not self.connected():
			return
		del self.control_sock
		del self.state_sock
		self.is_connected = False

	def got_controlgw_data(self):
		datagram, host, port = self.control_sock.readDatagram(4096)
		try:
			self.controlgw_handlers[ord(datagram[0])](datagram, host, port)
		except KeyError:
			pass

	def handle_cgw_connected(self):
		self.control_sock.sendCommand(ControlGw.command_id['Ping'], 'Connecting')

	def handle_progress_updated(self):
		if self.progress.value() == self.progress.maximum():
			del self.progress
			self.is_connected = True

	def handle_cgw_pong(self, datagram, host, port):
		if datagram[1:] == 'Connecting':
			print 'Got pong from command gw, successful connection.'
			self.progress.setValue(self.progress.value()+1)
			self.handle_progress_updated()

