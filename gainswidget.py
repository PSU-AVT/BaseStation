from PyQt4 import QtGui

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
	def __init__(self):
		super(CompleteStateWidget, self).__init__()
		mainHLayout = QtGui.QHBoxLayout()
		for name in ('Roll', 'Pitch', 'Yaw', 'X', 'Y', 'Z'):
			mainHLayout.addWidget(StateWidget(name))
		self.setLayout(mainHLayout)

class GainsWidget(QtGui.QWidget):
	def __init__(self):
		super(GainsWidget, self).__init__()
		self.setWindowTitle("Control Gains")

		self.p_statewidget = CompleteStateWidget()
		self.i_statewidget = CompleteStateWidget()
		self.d_statewidget = CompleteStateWidget()

		mainVLayout = QtGui.QVBoxLayout()
		groupbox = QtGui.QGroupBox("P")
		hlayout = QtGui.QHBoxLayout()
		hlayout.addWidget(self.p_statewidget)
		groupbox.setLayout(hlayout)
		mainVLayout.addWidget(groupbox)

		groupbox = QtGui.QGroupBox("I")
		hlayout = QtGui.QHBoxLayout()
		hlayout.addWidget(self.i_statewidget)
		groupbox.setLayout(hlayout)
		mainVLayout.addWidget(groupbox)

		groupbox = QtGui.QGroupBox("D")
		hlayout = QtGui.QHBoxLayout()
		hlayout.addWidget(self.d_statewidget)
		groupbox.setLayout(hlayout)
		mainVLayout.addWidget(groupbox)

		self.setLayout(mainVLayout)

