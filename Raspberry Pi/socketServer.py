
import socket
import thread

class socketServer(object):

    def __init__(self, host, port, connEventHandler):
        self.HOST = host
        self.PORT = port
        self.connEvent = connEventHandler

    def StartServer(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created'
        #print socket.gethostname()

        try:
            self.s.bind((socket.gethostbyname(self.HOST), self.PORT))
        except socket.error , msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            raise

        print 'Socket bind complete'

        self.s.listen(10)
        print 'Socket now listening'
        self.ServerListen()

    def CloseServer(self):
        self.s.close()

    def ServerListen(self):
        while 1:
            #wait to accept a connection
            conn, addr = self.s.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])

            #start new thread
            #thread.start_new_thread(self.handleConn ,(conn,))
            self.handleConn(conn)

    def handleConn(self, conn):
        while True:

            #Receiving from client
            data = conn.recv(1024)
            if not data:
                print 'connection closed, stop listening'
                break

            if self.connEvent:
                thread.start_new_thread(self.connEvent, (data, ))

        conn.close()
