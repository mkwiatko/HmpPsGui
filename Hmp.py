import numpy   as np
import serial
import os.path
from os import path


class Hmp():
   
   def __init__(self):
      self.ser = 0
      self.connected = False
   
   
   def connectSerial(self, serialDev = '/dev/ttyUSB0'):
      if path.exists(serialDev):
         self.ser = serial.Serial(
            port=serialDev,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
         )
      
         if self.ser.isOpen():
            print('Opened %s' %(serialDev))
            self.connected = True
         else:
            print('Failed to open %s' %(serialDev))
            self.connected = False
   
   def getId(self):
      if self.connected:
         self.ser.flushInput()
         cmd = '*IDN?\n'
         self.ser.write(cmd.encode())
         return self.ser.readline()
   
   def getOutput(self,channel):
      if self.connected:
         self.ser.flushInput()
         cmd = 'INSTrument:NSELect '+ str(channel+1) +'\n'
         self.ser.write(cmd.encode())
         cmd = 'OUTPut?\n'
         self.ser.write(cmd.encode())
         resp = self.ser.readline().decode("utf-8")
         if '1' in resp:
            return True
         else:
            return False
         #return self.ser.readline().decode("utf-8")
      else:
         return False
   
   def setOutput(self,channel,state):
      if self.connected:
         self.ser.flushInput()
         cmd = 'INSTrument:NSELect '+ str(channel+1) +'\n'
         self.ser.write(cmd.encode())
         if state:
            cmd = 'OUTPut:SELect 1\n'
         else:
            cmd = 'OUTPut:SELect 0\n'
         self.ser.write(cmd.encode())
      
   def getVoltage(self,channel):
      if self.connected:
         self.ser.flushInput()
         cmd = 'INSTrument:NSELect '+ str(channel+1) +'\n'
         self.ser.write(cmd.encode())
         cmd = 'VOLTage?\n'
         self.ser.write(cmd.encode())
         return self.ser.readline().decode("utf-8")
   
   def setVoltage(self,channel,voltage):
      if self.connected:
         self.ser.flushInput()
         cmd = 'INSTrument:NSELect '+ str(channel+1) +'\n'
         self.ser.write(cmd.encode())
         cmd = 'VOLTage %s\n'%voltage
         self.ser.write(cmd.encode())
   
   def getCurrent(self,channel):
      if self.connected:
         self.ser.flushInput()
         cmd = 'INSTrument:NSELect '+ str(channel+1) +'\n'
         self.ser.write(cmd.encode())
         cmd = 'CURRent?\n'
         self.ser.write(cmd.encode())
         return self.ser.readline().decode("utf-8")
   
   def setCurrent(self,channel,current):
      if self.connected:
         self.ser.flushInput()
         cmd = 'INSTrument:NSELect '+ str(channel+1) +'\n'
         self.ser.write(cmd.encode())
         cmd = 'CURRent %s\n'%current
         self.ser.write(cmd.encode())
   
   def measureVoltage(self,channel):
      if self.connected:
         self.ser.flushInput()
         cmd = 'INSTrument:NSELect '+ str(channel+1) +'\n'
         self.ser.write(cmd.encode())
         cmd = 'MEASure:VOLTage?\n'
         self.ser.write(cmd.encode())
         resp = self.ser.readline().decode("utf-8")
         resp = resp.replace('\n','')
         return resp
      else:
         return '0.0'
   
   def measureCurrent(self,channel):
      if self.connected:
         self.ser.flushInput()
         cmd = 'INSTrument:NSELect '+ str(channel+1) +'\n'
         self.ser.write(cmd.encode())
         cmd = 'MEASure:CURRent?\n'
         self.ser.write(cmd.encode())
         resp = self.ser.readline().decode("utf-8")
         resp = resp.replace('\n','')
         return resp
      else:
         return '0.0'
   
   