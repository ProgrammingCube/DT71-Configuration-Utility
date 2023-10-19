import sys, os, re, time, math
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, pyqtSlot

import pyqtgraph as pq

form_class = uic.loadUiType("main.ui")[0]

# Define a dictionary to store the variables and their values
config_data = {}

# Define lists to store USER_WAVEFORM, CALRB_K0, and CALRB_K1 data
user_waveform_data = []
calrb_k0_data = []
calrb_k1_data = []

# Define a variable to track the current section

# Define a regex pattern for matching variable assignments with or without commas
variable_pattern = r'(\w+)\s*=\s*(.*?)(?:\n|,|})'

filename = ""

class mainWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent=None):
        self.current_section = None
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
        filename = fname[0]
        # Open the configuration file for reading
        with open(filename, 'r') as file:
            for line in file:
                if "USER_WAVEFORM" in line:
                    self.current_section = "USER_WAVEFORM"
                    user_waveform_data.append(line.strip())
                elif "CALRB_K0" in line:
                    self.current_section = "CALRB_K0"
                    calrb_k0_data.extend(re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?', line))
                elif "CALRB_K1" in line:
                    self.current_section = "CALRB_K1"
                    calrb_k1_data.extend(re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?', line))
                elif self.current_section:
                    if '}' in line:
                        self.current_section = None
                    else:
                        if self.current_section == "USER_WAVEFORM":
                            user_waveform_data.append(line.strip())
                else:
                    match = re.match(variable_pattern, line)
                    if match:
                        variable_name, value = match.groups()
                        config_data[variable_name] = value

        user_waveform_data = user_waveform_data[1:]
        calrb_k0_data = calrb_k0_data[1:]
        calrb_k1_data = calrb_k1_data[1:]

        # Display the parsed data (config_data, user_waveform_data, calrb_k0_data, calrb_k1_data)
        print("config_data:")
        print(config_data)
        print("\nuser_waveform_data:")
        print(user_waveform_data)
        print("\ncalrb_k0_data:")
        print(calrb_k0_data)
        print("\ncalrb_k1_data:")
        print(calrb_k1_data)

    def saveFile(self):
        # Read the original configuration file
        print("Save clicked")

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