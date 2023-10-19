import sys, os, re, time, math
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, pyqtSlot

import pyqtgraph as pq

form_class = uic.loadUiType("main.ui")[0]

config_data = {}

class mainWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.resetDeviceButton.clicked.connect(self.resetDeviceButton_clicked)
        self.setDeviceButton.clicked.connect(self.setDeviceButton_clicked)

        self.actionOpen_File.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)

        self.initUI()
    
    def initUI(self):
        #self.statusBar().showMessage('When you : bottom text')
        self.show()
    
    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', os.path.dirname(os.path.abspath(__file__)))
        with open(fname[0], 'r') as file:
            capturing = False
            waveform_data = []
            for line in file:
                if capturing:
                    if '}' in line:
                        capturing = False
                        waveform_data.append(line)
                    else:
                        waveform_data.append(line)
                else:
                    match = re.match(r'(\w+)\s*=\s*(.*?)(?:\n|,|})', line)
                    if match:
                        variable_name, value = match.groups()
                        config_data[variable_name] = value
                    if '{' in line:
                        capturing = True
                        waveform_data.append(line)

        # Combine the lines within {} to form the complete USER_WAVEFORM value
        config_data['USER_WAVEFORM'] = ''.join(waveform_data)
        print(config_data)

    def saveFile(self):
        # hey

    @pyqtSlot()
    def resetDeviceButton_clicked(self):
        print("Reset Button clicked!")

    @pyqtSlot()
    def setDeviceButton_clicked(self):
        print("Set Button clicked!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex  = mainWindow()
    sys.exit(app.exec_())