from PyQt4 import QtCore, QtGui
import struct

class StateWidget(QtGui.QWidget):
	def __init__(self, desc):
		super(StateWidget, self).__init__()
		self.label = QtGui.QLabel(desc)
		self.spin_box = QtGui.QSpinBox()
		vlayout = QtGui.QVBoxLayout()
		vlayout.addWidget(self.label)
		vlayout.addWidget(self.spin_box)
		self.setLayout(vlayout)

class CompleteStateWidget(QtGui.QWidget):
	changed = QtCore.pyqtSignal()
	scale_factor = .001

	def __init__(self):
		super(CompleteStateWidget, self).__init__()
		self.roll_statewidget = StateWidget('Roll')
		self.pitch_statewidget = StateWidget('Pitch')
		self.yaw_statewidget = StateWidget('Yaw')

		top_h_layout = QtGui.QHBoxLayout()
		for w in (self.roll_statewidget, self.pitch_statewidget, self.yaw_statewidget):
			top_h_layout.addWidget(w)
			w.spin_box.valueChanged.connect(self.valueChanged)

		self.x_statewidget = StateWidget('X')
		self.y_statewidget = StateWidget('Y')
		self.z_statewidget = StateWidget('Z')
		bottom_h_layout = QtGui.QHBoxLayout()
		for w in (self.x_statewidget, self.y_statewidget, self.z_statewidget):
			bottom_h_layout.addWidget(w)
			w.spin_box.valueChanged.connect(self.valueChanged)

		v_layout = QtGui.QVBoxLayout()
		v_layout.addLayout(top_h_layout)
		v_layout.addLayout(bottom_h_layout)
		self.setLayout(v_layout)

	def valueChanged(self, val):
		self.changed.emit()

	def toBinaryStateString(self):
		widgets = (self.roll_statewidget, self.pitch_statewidget, self.yaw_statewidget, self.x_statewidget, self.y_statewidget, self.z_statewidget)
		scaled_vals = [w.spin_box.value() * self.scale_factor for w in widgets]
		return struct.pack('ffffff', *scaled_vals)

class GainsWidget(QtGui.QWidget):
	def __init__(self):
		super(GainsWidget, self).__init__()
		self.setWindowTitle("Control Gains")

		self.p_gains = CompleteStateWidget()
		self.i_gains = CompleteStateWidget()
		self.d_gains = CompleteStateWidget()

		mainVLayout = QtGui.QVBoxLayout()
		groupbox = QtGui.QGroupBox("P")
		hlayout = QtGui.QHBoxLayout()
		hlayout.addWidget(self.p_gains)
		groupbox.setLayout(hlayout)
		mainVLayout.addWidget(groupbox)

		groupbox = QtGui.QGroupBox("I")
		hlayout = QtGui.QHBoxLayout()
		hlayout.addWidget(self.i_gains)
		groupbox.setLayout(hlayout)
		mainVLayout.addWidget(groupbox)

		groupbox = QtGui.QGroupBox("D")
		hlayout = QtGui.QHBoxLayout()
		hlayout.addWidget(self.d_gains)
		groupbox.setLayout(hlayout)
		mainVLayout.addWidget(groupbox)

		self.setLayout(mainVLayout)

