from PyQt4 import QtGui

import attenuationwidget
import connectionmanager
import connectdialog
import joystick
import motors
import gainswidget

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.conn_mgr = connectionmanager.ConnectionManager()
		self.setupActions()
		self.initUi()

		self.state_tag_handlers = {
			'LlfcStateMotors': self.state_motors,
			'LlfcStateAttenuation': self.state_attenuation,
		}

	def setupActions(self):
		openJoysickAction = QtGui.QAction('Open Joystick', self)
		openJoysickAction.setStatusTip('Open joystick to use for controlling quadcopter')
		openJoysickAction.triggered.connect(self.show_open_joystick)

		closeJoystickAction = QtGui.QAction('Close Joystick', self)
		closeJoystickAction.setStatusTip('Close the currently open joystick')
		closeJoystickAction.setEnabled(False)

		connectAction = QtGui.QAction('&Connect', self)
		connectAction.setStatusTip('Connect to the quadcopter')
		connectAction.triggered.connect(self.show_connect)
		self.connectAction = connectAction

		disconnectAction = QtGui.QAction('&Disconnect', self)
		disconnectAction.setStatusTip('Disconnect from the quadcopter')
		disconnectAction.triggered.connect(self.conn_mgr.do_disconnect)
		self.disconnectAction = disconnectAction

		exitAction = QtGui.QAction('&Exit', self)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(QtGui.qApp.quit)

		quadcopterOnAction = QtGui.QAction('Turn On', self)
		quadcopterOnAction.setStatusTip('Turn on the Quadcopter')
		quadcopterOnAction.setEnabled(False)
		quadcopterOnAction.triggered.connect(self.on_turn_on)
		self.quadcopterOnAction = quadcopterOnAction

		quadcopterOffAction = QtGui.QAction('Turn Off', self)
		quadcopterOffAction.setStatusTip('Turn off the Quadcopter')
		quadcopterOffAction.setEnabled(False)
		quadcopterOffAction.triggered.connect(self.on_turn_off)
		self.quadcopterOffAction = quadcopterOffAction

		menubar = self.menuBar()
		fileMenu = menubar.addMenu("&File")
		fileMenu.addAction(openJoysickAction)
		fileMenu.addAction(closeJoystickAction)
		fileMenu.addSeparator()
		fileMenu.addAction(connectAction)
		fileMenu.addAction(disconnectAction)
		fileMenu.addSeparator()
		fileMenu.addAction(exitAction)

		quadcopterMenu = menubar.addMenu('Quadcopter')
		quadcopterMenu.addAction(quadcopterOnAction)
		quadcopterMenu.addAction(quadcopterOffAction)

		self.conn_mgr.validConnection.connect(self.on_connect)
		self.conn_mgr.disconnected.connect(self.on_disconnect)

	def initUi(self):
		self.setWindowTitle('Quadcopter BaseStation')

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

		attenLayout = QtGui.QVBoxLayout()
		attenLayout.addWidget(stateGroupBox)
		attenLayout.addWidget(spGroupBox)

		motorsGbLayout = QtGui.QVBoxLayout()
		motorsGbLayout.addWidget(motors.MotorsWidget())

		motorsGroupBox = QtGui.QGroupBox("Motors")
		motorsGroupBox.setLayout(motorsGbLayout)

		rightVLayout = QtGui.QVBoxLayout()
		rightVLayout.addWidget(motorsGroupBox)
		rightVLayout.addStretch()

		self.gainswidget = gainswidget.GainsWidget()

		mainHLayout = QtGui.QHBoxLayout()
		mainHLayout.addWidget(self.gainswidget)
		mainHLayout.addLayout(attenLayout)
		mainHLayout.addLayout(rightVLayout)

		mainWidget = QtGui.QWidget()
		mainWidget.setLayout(mainHLayout)

		self.setCentralWidget(mainWidget)

		self.on_disconnect()

	def show_connect(self):
		cd = connectdialog.ConnectDialog()
		if cd.exec_():
			self.conn_mgr.do_connect(cd.hostname())

	def show_open_joystick(self):
		jd = joystick.OpenJoystickDialog()
		jd.exec_()

	def on_disconnect(self):
		self.statusBar().showMessage("Disconnected.")
		self.connectAction.setEnabled(True)
		self.disconnectAction.setEnabled(False)
		self.quadcopterOffAction.setEnabled(True)
		self.quadcopterOnAction.setEnabled(True)

	def on_connect(self):
		self.statusBar().showMessage("Connected.")
		self.connectAction.setEnabled(False)
		self.disconnectAction.setEnabled(True)
		self.quadcopterOffAction.setEnabled(True)
		self.quadcopterOnAction.setEnabled(True)

	def on_turn_off(self):
		self.conn_mgr.try_command('Off')

	def on_turn_on(self):
		self.conn_mgr.try_command('On')

	def state_attenuation(self, data):
		print 'Got attenuation'

	def state_motors(self, data):
		print 'Got motors'

