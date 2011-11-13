from PyQt4 import QtCore, QtGui

class ConnectionManager(QtCore.QObject):
	def __init__(self):
		super(ConnectionManager, self).__init__()
		self.timeout_secs = 10
		self.is_connected = False

	def connected(self):
		return self.is_connected

	def do_connect(self, host):
		self.progress = QtGui.QProgressDialog("Connecting to quadcopter...", "Cancel", 0, self.timeout_secs)
		self.progress.setVisible(True)

