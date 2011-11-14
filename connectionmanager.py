import time
import struct

from PyQt4 import QtCore, QtGui, QtNetwork

class UdpClient(QtNetwork.QUdpSocket):
	def __init__(self):
		super(UdpClient, self).__init__()
	
	def setDestination(self, hostname, port):
		self.hostname = hostname
		self.port = port
		self.ha = QtNetwork.QHostAddress(self.hostname)
		self.connectToHost(hostname, port)

	def sendData(self, data):
		self.writeDatagram(data, self.ha, self.port)

class ControlGw(UdpClient):
	command_id = {
		'Ping': 1 }
	response_id = {
		'Pong': 1
	}

	def __init__(self):
		super(ControlGw, self).__init__()

	def sendCommand(self, command_id, data):
		self.sendData(chr(command_id) + data)

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
		self.control_sock.setDestination('psu-avt.dyndns.org', 8091)
		self.control_sock.sendCommand(ControlGw.command_id['Ping'], 'Connecting')

		self.state_sock = StatePublisher()
		self.state_sock.setDestination('psu-avt.dyndns.org', 8092)
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

	def handle_progress_updated(self):
		if self.progress.value() == self.progress.maximum():
			del self.progress
			self.is_connected = True

	def handle_cgw_pong(self, datagram, host, port):
		if datagram[1:] == 'Connecting' and not self.connected():
			self.progress.setValue(self.progress.value()+1)
			self.handle_progress_updated()

