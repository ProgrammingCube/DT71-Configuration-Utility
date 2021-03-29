import sys, os, time, math
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, pyqtSlot

import pyqtgraph as pq

form_class = uic.loadUiType("main.ui")[0]

class mainWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.initUI()
    
    def initUI(self):
        #self.statusBar().showMessage('When you : bottom text')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex  = mainWindow()
    sys.exit(app.exec_())