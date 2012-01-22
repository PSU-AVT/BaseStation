from PyQt4 import QtCore, QtGui

class MotorWidget(QtGui.QWidget):
	def __init__(self, label):
		super(MotorWidget, self).__init__()
		self.throttle = 0
		self.label = label
		self.setupUi()

	def setupUi(self):
		self.slider = QtGui.QSlider(0x0)
		self.slider.setEnabled(False)
		self.slider.setRange(0, 100)

		self.throttleLabel = QtGui.QLabel('0 %')

		vLayout = QtGui.QVBoxLayout()
		vLayout.addWidget(QtGui.QLabel(self.label))
		vLayout.addWidget(self.slider)
		vLayout.addWidget(self.throttleLabel)

		self.setLayout(vLayout)

	def setThrottle(self, throttle):
		self.throttle = throttle
		self.throttleLabel.setText(str(throttle * 100) + ' %')
		self.slider.setSliderPosition(int(throttle*100))

class MotorsWidget(QtGui.QWidget):
	def __init__(self):
		super(MotorsWidget, self).__init__()
		self.motor_widgets = [
			MotorWidget("F"),
			MotorWidget("L"),
			MotorWidget("R"),
			MotorWidget("B") ]
		self.setupUi()

	def setupUi(self):
		hLayout = QtGui.QHBoxLayout()
		for motor in self.motor_widgets:
			hLayout.addWidget(motor)
			motor.setEnabled(False)
		self.setLayout(hLayout)

	def setMotorThrottle(self, ndx, throttle):
		self.motor_widgets[ndx].setThrottle(throttle)

