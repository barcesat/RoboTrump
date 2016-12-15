from TorsoInterface import Torso
import motorctl
from trumpvoice import TrumpVoice
from InsultsFileReader import InsultsFileReader
import picam
import thread 

HOST = "192.168.0.100"
#HOST = "localhost"
PORT = 8888
TORSO_USB_PORT = 'COM14'
LOOP_DELAY = 0.5
VOICE_PORT = '/dev/ttyS0'
VOICE_PORT_RATE = 9600
VOICE_PORT_TIMEOUT = 1

from signal import *
import sys, time
torso = Torso(TORSO_USB_PORT, LOOP_DELAY)
voice = TrumpVoice(VOICE_PORT, VOICE_PORT_RATE, VOICE_PORT_TIMEOUT)
insults = InsultsFileReader()

def faceFound(score, position):
    print('found face, finding insult')
    insultText, playFile = insults.getInsult(score)
    voice.RunText(insultText)
    if playFile:
        print("insult play file ",  playFile)
           #torso.RunPlay(playFile)

def clean(*args):
    print "clean up and closing"
    motorctl.cleanup()
    #server.server_close()
    soc.CloseServer()
    voice.CloseSocket()
    torso.Close()
    sys.exit(0)

currState = ["idle"]
camThread = None

def eventFlow(data):
    try:
	    print('got command: ', data)
	    if data.startswith("speech"):
		voice.RunSpeech()
	        #torso.RunPlay('duck.csv')
	        # call text-to-speech
	
	    elif data.startswith("greet"):
		currState[0] = "greet"
	        camThread = thread.start_new_thread(picam.findFace, (faceFound, currState ))
		#picam.findFace(faceFound, currState)
	
	    elif data.startswith("stop greet"):
		print("stopping greet")
		currState[0] = "idle"
	
	    elif data.startswith("forward"):
	        motorctl.forward()
	
	    elif data.startswith("backwards"):
	        motorctl.reverse()
	
	    elif data.startswith("left"):
	        motorctl.TurnLeft()
	
	    elif data.startswith("right"):
	        motorctl.TurnRight()
	
	    elif data.startswith("stop"):
	        motorctl.stop()
	
	    else:
	        print ('command not recognized')
    except Exception as inst: 
	clean()

from socketServer import socketServer
soc = socketServer(HOST, PORT, eventFlow)
soc.StartServer()




for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
    signal(sig, clean)


print 'end'