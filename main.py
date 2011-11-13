import sys
from PyQt4 import QtGui

import mainwindow

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)

	mw = mainwindow.MainWindow()
	mw.show()

	sys.exit(app.exec_())
