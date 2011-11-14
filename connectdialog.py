from PyQt4 import QtGui

class ConnectDialog(QtGui.QDialog):
	def __init__(self):
		super(ConnectDialog, self).__init__()
		self.setupUi()

	def setupUi(self):
		self.hostnameLineEdit = QtGui.QLineEdit()

		hostnameLayout = QtGui.QHBoxLayout()
		hostnameLayout.addWidget(QtGui.QLabel("Hostname:"))
		hostnameLayout.addWidget(self.hostnameLineEdit)

		cancelButton = QtGui.QPushButton("Cancel")
		cancelButton.clicked.connect(self.reject)
		connectButton = QtGui.QPushButton("Connect")
		connectButton.clicked.connect(self.accept)

		buttonLayout = QtGui.QHBoxLayout()
		buttonLayout.addWidget(cancelButton)
		buttonLayout.addWidget(connectButton)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addLayout(hostnameLayout)
		mainLayout.addLayout(buttonLayout)
		self.setLayout(mainLayout)

	def hostname(self):
		return self.hostnameLineEdit.text()

