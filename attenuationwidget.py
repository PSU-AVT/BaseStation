from PyQt4 import QtGui

import angledial

class SingleAxisWidget(QtGui.QWidget):
	def __init__(self, dial, label):
		super(SingleAxisWidget, self).__init__()
		v_layout = QtGui.QVBoxLayout()
		v_layout.addWidget(QtGui.QLabel(label))
		v_layout.addWidget(dial)
		self.setLayout(v_layout)

class AttenuationWidget(QtGui.QWidget):
	def __init__(self):
		super(AttenuationWidget, self).__init__()
		self.roll = 0.0
		self.pitch = 0.0
		self.yaw = 0.0
		self.setupUi()

	def setupUi(self):
		self.roll_dial = angledial.AngleDial()
		self.pitch_dial = angledial.AngleDial()
		self.yaw_dial = angledial.AngleDial()

		h_layout = QtGui.QHBoxLayout()
		h_layout.addWidget(SingleAxisWidget(self.roll_dial, "Roll"))
		h_layout.addWidget(SingleAxisWidget(self.pitch_dial, "Pitch"))
		h_layout.addWidget(SingleAxisWidget(self.yaw_dial, "Yaw"))

		self.setLayout(h_layout)

	def setRoll(self, value):
		self.roll_dial.setAngle(value)

	def setPitch(self, value):
		self.pitch_dial.setAngle(value)

	def setYaw(self, value):
		self.yaw_dial.setAngle(value)

	def setInputAllowed(self, value):
		for dial in (self.roll_dial, self.pitch_dial, self.yaw_dial):
			dial.setEnabled(value)

