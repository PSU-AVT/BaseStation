import os
import struct
from PyQt4 import QtGui, QtCore

def available_joysticks():
	ret = []
	for path in os.listdir('/dev/input'):
		if path.startswith(''):
			ret.append('/dev/input/'+path)
	return ret

class JoystickEvent(object):
        def __init__(self, time, value, event_type, number):
                self.time = time
                self.value = value
                self.event_type = event_type
                self.number = number

class QJoystick(QtCore.QSocketNotifier):
	# QJoystick.gotEvent(JoystickEvent)
	gotEvent = QtCore.pyqtSignal(JoystickEvent)
	maxvals = {}

	def __init__(self, joystick_file):
		super(QJoystick, self).__init__(joystick_file.fileno(), 0)
		self.joystick_file = joystick_file
		self.setEnabled(True)
		self.activated.connect(self.onRead)

	def onRead(self, sock):
		bin_data = struct.unpack("IhBB", os.read(sock, 8))
		ev = JoystickEvent(*bin_data)
		if ev.event_type not in self.maxvals:
			self.maxvals[ev.event_type] = {}

		try:
			maxval = self.maxvals[ev.event_type][ev.number]
			ev.value = ev.value / 32768.0
			self.gotEvent.emit(ev)
		except KeyError:
			self.maxvals[ev.event_type][ev.number] = ev.value

class ThrottledEventsJoystick(QJoystick):
	throttledEvent = QtCore.pyqtSignal(JoystickEvent)

	def __init__(self, joystick_file, max_send_dt=0.05):
		super(ThrottledEventsJoystick, self).__init__(joystick_file)
		self.ev_timer = QtCore.QTimer()
		self.ev_timer.setInterval(int(max_send_dt*1000))
		self.ev_timer.setSingleShot(False)
		self.ev_timer.timeout.connect(self.timeout)
		self.gotEvent.connect(self.got_event)

	def got_event(self, event):
		if not self.ev_timer.isActive():
			self.throttledEvent.emit(event)
			self.last_sent_event = event
			self.latest_event = event
			self.ev_timer.start()
		else:
			self.latest_event = event

	def timeout(self):
		if self.latest_event == self.last_sent_event:
			self.throttledEvent.emit(self.latest_event)
			self.ev_timer.stop()
		else:
			self.throttledEvent.emit(self.latest_event)
			self.last_sent_event = self.latest_event

class OpenJoystickDialog(QtGui.QDialog):
	def __init__(self):
		super(OpenJoystickDialog, self).__init__()
		self.setupUi()

	def joystickPath(self):
		return self.pathComboBox.currentText()

	def setupUi(self):
		self.pathComboBox = QtGui.QComboBox()
		self.pathComboBox.activated.connect(self.updateOpenButton)

		rescanJoysticksButton = QtGui.QPushButton("Rescan")
		rescanJoysticksButton.clicked.connect(self.rescanJoysticks)

		openButton = QtGui.QPushButton("Open")
		openButton.clicked.connect(self.accept)
		self.openButton = openButton

		cancelButton = QtGui.QPushButton("Cancel")
		cancelButton.clicked.connect(self.reject)

		pathHBox = QtGui.QHBoxLayout()
		pathHBox.addWidget(self.pathComboBox)
		pathHBox.addWidget(rescanJoysticksButton)

		buttonHBox = QtGui.QHBoxLayout()
		buttonHBox.addWidget(cancelButton)
		buttonHBox.addWidget(openButton)

		mainVBox = QtGui.QVBoxLayout()
		mainVBox.addWidget(QtGui.QLabel("Select joystick"))
		mainVBox.addLayout(pathHBox)
		mainVBox.addLayout(buttonHBox)

		self.setLayout(mainVBox)

		self.rescanJoysticks()
		self.updateOpenButton()

	def rescanJoysticks(self):
		self.pathComboBox.clear()
		for path in available_joysticks():
			self.pathComboBox.addItem(path)

	def updateOpenButton(self):
		self.openButton.setEnabled(self.pathComboBox.currentText().isEmpty() == False)

