from PyQt4 import QtGui

class AngleDial(QtGui.QDial):
	def __init__(self):
		super(AngleDial, self).__init__()
		self.setSingleStep(25)
		self.setPageStep(1)
		self.setNotchesVisible(True)
		self.setRange(-3000, 3000)
		self.setAngle(0.0)

	def setAngle(self, angle):
		if angle > 3:
			angle = 3
		self.setSliderPosition(int(angle*1000))

	def toRadians(self):
		return self.value() * (6.283 / 3600)

