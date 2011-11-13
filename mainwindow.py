from PyQt4 import QtGui

import gyrowidget

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.initUi()

	def initUi(self):
		self.setWindowTitle('Quadcopter BaseStation')
		self.gyro_widget = gyrowidget.GyroWidget()
		self.setCentralWidget(self.gyro_widget)
