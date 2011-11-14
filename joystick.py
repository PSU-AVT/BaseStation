import os
from PyQt4 import QtGui

def available_joysticks():
	ret = []
	for path in os.listdir('/dev/input'):
		if path.startswith('js'):
			ret.append('/dev/input/'+path)
	return ret

class OpenJoystickDialog(QtGui.QDialog):
	def __init__(self):
		super(OpenJoystickDialog, self).__init__()
		self.setupUi()

	def setupUi(self):
		self.pathComboBox = QtGui.QComboBox()

		rescanJoysticksButton = QtGui.QPushButton("Rescan")
		rescanJoysticksButton.clicked.connect(self.rescanJoysticks)

		openButton = QtGui.QPushButton("Open")
		openButton.setEnabled(False)
		openButton.clicked.connect(self.accept)

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

	def rescanJoysticks(self):
		self.pathComboBox.clear()
		for path in available_joysticks():
			self.pathComboBox.addItem(path)

