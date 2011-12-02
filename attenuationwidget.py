import struct

from PyQt4 import QtCore, QtGui

import angledial

class SingleAxisWidget(QtGui.QWidget):
	def __init__(self, dial, label):
		super(SingleAxisWidget, self).__init__()
		v_layout = QtGui.QVBoxLayout()
		v_layout.addWidget(QtGui.QLabel(label))
		v_layout.addStretch()
		v_layout.addWidget(dial)
		v_layout.addStretch()
		self.setLayout(v_layout)

class AttenuationWidget(QtGui.QWidget):
	changed = QtCore.pyqtSignal()

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
		self.x_spinbox = QtGui.QSpinBox()
		self.y_spinbox = QtGui.QSpinBox()
		self.z_spinbox = QtGui.QSpinBox()

		self.roll_dial.valueChanged.connect(self.onValChanged)
		self.pitch_dial.valueChanged.connect(self.onValChanged)
		self.yaw_dial.valueChanged.connect(self.onValChanged)

		top_h_layout = QtGui.QHBoxLayout()
		top_h_layout.addWidget(SingleAxisWidget(self.roll_dial, "Roll"))
		top_h_layout.addWidget(SingleAxisWidget(self.pitch_dial, "Pitch"))
		top_h_layout.addWidget(SingleAxisWidget(self.yaw_dial, "Yaw"))

		bottom_h_layout = QtGui.QHBoxLayout()
		bottom_h_layout.addWidget(SingleAxisWidget(self.x_spinbox, "X"))
		bottom_h_layout.addWidget(SingleAxisWidget(self.y_spinbox, "Y"))
		bottom_h_layout.addWidget(SingleAxisWidget(self.z_spinbox, "Z"))

		v_layout = QtGui.QVBoxLayout()
		v_layout.addLayout(top_h_layout)
		v_layout.addLayout(bottom_h_layout)

		self.setLayout(v_layout)

	def setRoll(self, value):
		self.roll_dial.setAngle(value)
		self.changed.emit()

	def setPitch(self, value):
		self.pitch_dial.setAngle(value)
		self.changed.emit()

	def setYaw(self, value):
		self.yaw_dial.setAngle(value)
		self.changed.emit()

	def setInputAllowed(self, value):
		for dial in (self.roll_dial, self.pitch_dial, self.yaw_dial, self.x_spinbox, self.y_spinbox, self.z_spinbox):
			dial.setEnabled(value)

	def toBinaryStateString(self):
		vals = [ x.toRadians() for x in (self.roll_dial, self.pitch_dial, self.yaw_dial) ] + [ x.value() for x in (self.x_spinbox, self.y_spinbox, self.z_spinbox) ]
		return struct.pack('ffffff', *vals)
		
	def onValChanged(self, val):
		self.changed.emit()

