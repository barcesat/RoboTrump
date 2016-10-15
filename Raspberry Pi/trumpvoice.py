import serial
import time
import csv


class TrumpVoice(object):
	
	def __init__(self, VOICE_PORT, VOICE_PORT_RATE, VOICE_PORT_TIMEOUT):
		self.VOICE_PORT = VOICE_PORT
		self.VOICE_PORT_RATE = VOICE_PORT_RATE
		self.VOICE_PORT_TIMEOUT = VOICE_PORT_TIMEOUT
		self.Open = False

	def OpenSocket(self):
		if self.Open:
			return

		try: 
			self.ser = serial.Serial(self.VOICE_PORT, self.VOICE_PORT_RATE, timeout=self.VOICE_PORT_TIMEOUT)
			print("opened serial voice port ", self.ser.name)
			self.Open = True
			#wakeup test
			self.ser.write('\n')
			#a = ser.read()
			#while (a != ':'):
			#    print(a)
			
			#talk setup
			self.ser.write('V14')
			self.ser.write('\n')
			#set speaking rate
			self.ser.write('W150')
			self.ser.write('\n')
			#set speaker
			self.ser.write('N4')
			self.ser.write('\n')

		except Exception as inst:
			print("failed open socket to voice", inst)
			raise

	def CloseSocket(self):
		if self.Open:
			self.ser.close()

	def RunSpeech(self):

		self.RunText2(">>Make Geek Con great again! We didn't have time for a speech!")
		'''
		self.RunText2(">>I know a lot of your projects failed. __Waa __waa. Unlike you,")
		self.RunText2(">>I am not a failure. I've probably never failed at anything in my entire life.")
		self.RunText2(">>You should try to be more like me.")
		self.RunText2(">>I came to talk to you today about robots.") 
		#self.RunText2(">>No I don't mean Hillary. Hahaha. I mean __foreign robots.") These robots are coming here and they are taking all the good jobs away from us. Are you just going to sit there and let it happen? And you know where these robots are made. Mexico. China. Have you ever seen one of these robots from China? Terrible. They're junk. Stop using them. I don't care if Ally Express is cheaper. Get a real bot like me! Don't be a loser.")
		self.RunText2(">>Next year at Geek Con, when I am president, I'm going to make some changes.")
                self.RunText2(">> __Believe me. Things are going to change.")
		self.RunText2(">>We're going to get rid of this silly rule about guns and explosions.") 
		self.RunText2(">>>>Oh no! The explosion is going to hurt me!<< Please. We're not babies.")
		self.RunText2(">>At least I'm not.<< Next year, with me running things, every project is going to explode.")
		self.RunText2(">>__Every __single __one. Also all this nonsense about the computer companies,")
                self.RunText2(">>Apple or Microsoft, Apple or Microsoft.")
		self.RunText2(">> Next year, you will all have Trump brand computers! Until then, don't forget.")
		self.RunText2(">>Vote Trump! Let's make Geek Con great again! I will make all of your wildest nightmares come true!")
		self.RunText2(">>Thank you beautiful people!")
		'''

	def RunText2(self, text):
		self.OpenSocket()
		#while(True):
		self.ser.write('S')
		#ser.write("Oh mare")
		self.ser.write(text)     # write a string
		self.ser.write('\n')
		a = self.ser.read()
		while (a != ':'):
			a = self.ser.read()
			#time.sleep(0.1)

	def RunText(self, text):
		self.OpenSocket()
		#while(True):
		self.ser.write('S')
		#ser.write("Oh mare")
		self.ser.write(text)     # write a string
		self.ser.write('\n')
    
#a = ser.read()
#while (a != ':'):
#    print(a)
#time.sleep(0.5)
