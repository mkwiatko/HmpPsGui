import time
import sys
try:
   from PyQt5.QtWidgets import *
   from PyQt5.QtCore    import *
   from PyQt5.QtGui     import *
except ImportError:
   from PyQt4.QtCore    import *
   from PyQt4.QtGui     import *

import numpy as np
import Hmp as hp


class Window(QMainWindow, QObject):
   
   
   def __init__(self, hmp):
      super(Window, self).__init__()    
      
      self.channels = 3
      
      self.hmp = hmp
      
      self.setGeometry(0,0,480,320)
      self.setWindowTitle("HMP GUI")
      
      self.timer = QTimer(self)
      self.timer.setInterval(1000)
      self.timer.timeout.connect(self.updateLabelsPeriodic)
      
      self.mainWidget = QWidget(self)
      
      self.connectButton = QPushButton("Connect")
      self.connectButton.clicked.connect(self.connectButtonClick)
      #self.connectButton.setFixedHeight(50)
      self.connectTbox = QLineEdit('/dev/ttyUSB0')
      hbox_0 = QHBoxLayout()
      hbox_0.addWidget(self.connectButton)
      hbox_0.addWidget(self.connectTbox)
      
      hbox_1 = QHBoxLayout()
      
      self.voltInput = [None] * self.channels
      self.currInput = [None] * self.channels
      self.enableButtons = [None] * self.channels
      self.voltMeas = [None] * self.channels
      self.currMeas = [None] * self.channels
      for i in range(self.channels):
         vbox = QVBoxLayout()
         
         self.enableButtons[i] = QPushButton("CH%d"%(i+1))
         self.enableButtons[i].setStyleSheet('QPushButton {color: red;}')
         self.enableButtons[i].clicked.connect(lambda _, b=i: self.enableButtonClick(num=b))
         
         voltLabel = QLabel()
         voltLabel.setAlignment(Qt.AlignCenter)
         voltLabel.setText('Voltage [V]')
         voltLabel.setFixedHeight(20)
         
         self.voltInput[i] = QLineEdit(self.hmp.getVoltage(i))
         self.voltInput[i].returnPressed.connect(lambda b=i: self.voltageEnter(num=b))
         
         currLabel = QLabel()
         currLabel.setAlignment(Qt.AlignCenter)
         currLabel.setText('Current [A]')
         currLabel.setFixedHeight(20)
         
         self.currInput[i] = QLineEdit(self.hmp.getCurrent(i))
         self.currInput[i].returnPressed.connect(lambda b=i: self.currentEnter(num=b))
         
         measLabel = QLabel()
         measLabel.setAlignment(Qt.AlignCenter)
         measLabel.setText('Measured')
         measLabel.setFixedHeight(20)
         
         self.voltMeas[i] = QLabel()
         self.voltMeas[i].setAlignment(Qt.AlignCenter)
         self.voltMeas[i].setText('%s [V]'%self.hmp.measureVoltage(i))
         self.voltMeas[i].setFixedHeight(20)
         
         self.currMeas[i] = QLabel()
         self.currMeas[i].setAlignment(Qt.AlignCenter)
         self.currMeas[i].setText('%s [A]'%self.hmp.measureCurrent(i))
         self.currMeas[i].setFixedHeight(20)
         
         vbox.addWidget(self.enableButtons[i])
         vbox.addWidget(voltLabel)
         vbox.addWidget(self.voltInput[i])
         vbox.addWidget(currLabel)
         vbox.addWidget(self.currInput[i])
         vbox.addWidget(measLabel)
         vbox.addWidget(self.voltMeas[i])
         vbox.addWidget(self.currMeas[i])
         hbox_1.addLayout(vbox)
      
      
      vbox = QVBoxLayout(self.mainWidget)
      vbox.addLayout(hbox_0)
      vbox.addLayout(hbox_1)
      
      self.mainWidget.setFocus()        
      self.setCentralWidget(self.mainWidget)
      
      self.show()
   
   def connectButtonClick(self):
      self.hmp.connectSerial(self.connectTbox.text())
      if self.hmp.connected:
         self.updateLabels()
         self.updateLabelsPeriodic()
         self.timer.start()
   
   def enableButtonClick(self, num):
      if self.hmp.getOutput(num):
         self.hmp.setOutput(num,False)
         self.enableButtons[num].setStyleSheet('QPushButton {color: red;}')
      else:
         self.hmp.setOutput(num,True)
         self.enableButtons[num].setStyleSheet('QPushButton {color: green;}')
   
   def voltageEnter(self, num):
      self.hmp.setVoltage(num, self.voltInput[num].text())
   
   def currentEnter(self, num):
      self.hmp.setCurrent(num, self.currInput[num].text())
   
   def updateLabels(self):
      for i in range(self.channels):
         self.voltInput[i].setText(self.hmp.getVoltage(i))
         self.currInput[i].setText(self.hmp.getCurrent(i))
         if self.hmp.getOutput(i):
            self.enableButtons[i].setStyleSheet('QPushButton {color: green;}')
         else:
            self.enableButtons[i].setStyleSheet('QPushButton {color: red;}')
   
   def updateLabelsPeriodic(self):
      for i in range(self.channels):
         self.voltMeas[i].setText('%s [V]'%self.hmp.measureVoltage(i))
         self.currMeas[i].setText('%s [A]'%self.hmp.measureCurrent(i))
   
if __name__ == '__main__':
   hmp = hp.Hmp()
   
   
   app = QApplication(sys.argv)
   gui = Window(hmp)
   app.exec()
