__author__ = 'zivla_000'
import serial
import time
from PlayFileReader import PlayListReader

class Torso(object):

    def __init__(self, USB_PORT, LOOP_DELAY):
        self.playListReader = PlayListReader()
	self.USB_PORT = USB_PORT
	self.LOOP_DELAY = LOOP_DELAY
	self.Open = False
        #self.OpenSocket()

    def OpenSocket(self):
        try:
            self.ser = serial.Serial(self.USB_PORT, 9600, timeout=1)
            self.Open = True
        except Exception as inst:
            print("failed open socket to Torso: ", inst)
            raise

    def RunPlay(self, playListName):
	if self.Open == False:
		self.OpenSocket()

        playList = self.playListReader.readPlayFile('test.csv')

        for row in playList:
            print("sending: ", row)
            self.ser.write(row['1'])
            self.ser.write(row['2'])
            self.ser.write(row['3'])
            self.ser.write(row['4'])
            self.ser.write(row['5'])
            self.ser.write(row['6'])
            self.ser.write(row['7'])
            self.ser.write(row['8'])
            time.sleep(self.LOOP_DELAY)

    def Close(self):
	if self.Open:
		self.ser.close()

    def RunPlay2(self, playList):
        for row in playList:
            print("sending: ", row)
            ser.write(row['1'])
            ser.write(row['2'])
            ser.write(row['3'])
            ser.write(row['4'])
            ser.write(row['5'])
            ser.write(row['6'])
            ser.write(row['7'])
            ser.write(row['8'])
            time.sleep(self.LOOP_DELAY)

