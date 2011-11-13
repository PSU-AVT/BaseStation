from PyQt4 import QtGui

import angledial

class GyroSingleAxisWidget(QtGui.QWidget):
	def __init__(self, dial, label):
		super(GyroSingleAxisWidget, self).__init__()
		v_layout = QtGui.QVBoxLayout()
		v_layout.addWidget(QtGui.QLabel(label))
		v_layout.addWidget(dial)
		self.setLayout(v_layout)

class GyroWidget(QtGui.QWidget):
	def __init__(self):
		super(GyroWidget, self).__init__()
		self.roll = 0.0
		self.pitch = 0.0
		self.yaw = 0.0
		self.setupUi()

	def setupUi(self):
		self.roll_dial = angledial.AngleDial()
		self.pitch_dial = angledial.AngleDial()
		self.yaw_dial = angledial.AngleDial()

		h_layout = QtGui.QHBoxLayout()
		h_layout.addWidget(GyroSingleAxisWidget(self.roll_dial, "Roll"))
		h_layout.addWidget(GyroSingleAxisWidget(self.pitch_dial, "Pitch"))
		h_layout.addWidget(GyroSingleAxisWidget(self.yaw_dial, "Yaw"))

		self.setLayout(h_layout)

