from PyQt4 import QtGui

import attenuationwidget
import connectionmanager
import connectdialog

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.conn_mgr = connectionmanager.ConnectionManager()
		self.initUi()

	def initUi(self):
		self.setWindowTitle('Quadcopter BaseStation')

		exitAction = QtGui.QAction('&Exit', self)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(QtGui.qApp.quit)

		connectAction = QtGui.QAction('&Connect', self)
		connectAction.setStatusTip('Connect to the quadcopter')
		connectAction.triggered.connect(self.show_connect)
		self.connectAction = connectAction

		disconnectAction = QtGui.QAction('&Disconnect', self)
		disconnectAction.setStatusTip('Disconnect from the quadcopter')
		disconnectAction.triggered.connect(self.conn_mgr.do_disconnect)
		self.disconnectAction = disconnectAction

		menubar = self.menuBar()
		fileMenu = menubar.addMenu("&File")
		fileMenu.addAction(connectAction)
		fileMenu.addAction(disconnectAction)
		fileMenu.addSeparator()
		fileMenu.addAction(exitAction)


		self.gyro_widget = attenuationwidget.AttenuationWidget()
		self.gyro_widget.setInputAllowed(False)

		self.atenn_setpoint_widget = attenuationwidget.AttenuationWidget()
		self.atenn_setpoint_widget.setInputAllowed(True)

		stateGroupBox = QtGui.QGroupBox("State")
		sgbLayout = QtGui.QVBoxLayout()
		sgbLayout.addWidget(self.gyro_widget)
		stateGroupBox.setLayout(sgbLayout)

		spGroupBox = QtGui.QGroupBox("Set Point")
		spLayout = QtGui.QHBoxLayout()
		spLayout.addWidget(self.atenn_setpoint_widget)
		spGroupBox.setLayout(spLayout)

		mainWidget = QtGui.QWidget()
		vLayout = QtGui.QVBoxLayout()
		vLayout.addWidget(stateGroupBox)
		vLayout.addWidget(spGroupBox)
		mainWidget.setLayout(vLayout)

		self.setCentralWidget(mainWidget)

		self.on_disconnect()

	def show_connect(self):
		cd = connectdialog.ConnectDialog()
		if cd.exec_():
			self.conn_mgr.do_connect(cd.hostname())

	def on_disconnect(self):
		self.statusBar().showMessage("Disconnected.")
		self.disconnectAction.setEnabled(False)


	def on_connect(self):
		self.statusBar().showMessage("Connected.")
		self.connectAction.setEnabled(False)
