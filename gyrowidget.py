from PyQt4 import QtGui

import angledial

class GyroWidget(QtGui.QWidget):
	def __init__(self):
		super(GyroWidget, self).__init__()
		self.roll = 0.0
		self.pitch = 0.0
		self.yaw = 0.0
		self.setupUi()

	def setupUi(self):
		self.roll_dial = angledial.AngleDial()

		h_layout = QtGui.QHBoxLayout()
		h_layout.addWidget(self.roll_dial)

		self.setLayout(h_layout)

