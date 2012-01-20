from PyQt4 import QtGui

class DebugConsole(QtGui.QTextEdit):
	def __init__(self, pubsub):
		super(DebugConsole, self).__init__()
		self.setReadOnly(True)
		pubsub.subscribeTo('LlfcDebug')
		pubsub.addHandler('LlfcDebug', self.gotDebugMsg)

	def gotDebugMsg(self, msg):
		self.debugMsg(msg.split(': ')[1])
		print msg

	def debugMsg(self, msg):
		self.append('<font color=\"green\">' + msg + '</font>' + '\n')

	def errorMsg(self, msg):
		self.append('<font color=\"red\">' + msg + '</font>' + '\n')

