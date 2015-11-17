"""
Listen to serial, return most recent numeric values
Lots of help from here:
http://stackoverflow.com/questions/1093598/pyserial-how-to-read-last-line-sent-from-serial-device
"""
from threading import Thread
import threading
import time
import serial
import Tkinter

last_received = ''
curspeed = 0
speedlast=0

def receiving(ser):
    global last_received
    global curspeed
    global speedlast
    buffer = ''

    app = MyTkApp()
    print 'now can continue running code while mainloop runs'
    while True:
        speed=ser.read(ser.inWaiting())
        buffer = buffer + speed
        if speed != speedlast:
            speedlast=speed
            print speedlast
        if (ser.isOpen()):
            ser.write(chr(curspeed))
        if '\n' in buffer:
            lines = buffer.split('\n') # Guaranteed to have at least 2 entries
            last_received = lines[-2]
            #If the Arduino sends lots of empty lines, you'll lose the
            #last filled line, so you could make the above statement conditional
            #like so: if lines[-2]: last_received = lines[-2]
            buffer = lines[-1]

class MyTkApp(threading.Thread):
    def mhello(self, event = None):
        global curspeed
        mtext=self.speed.get()
        curspeed=int(mtext)/100
        mlabel2=Tkinter.Label(self.root,text=str(mtext)).pack()
        return
    def getspeed(self):
        return self.speed.get()
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
    def callback(self):
        self.root.quit()
    def run(self):
		self.root=Tkinter.Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.callback)
		self.root.title("Group 3: Controls Project")
		self.speed = Tkinter.StringVar()
		self.root.geometry('450x150+500+300')
		#mbutton = Tkinter.Button(self.root,text='OK',command=self.mhello,fg='black',bg='grey').pack()
		mlabel1=Tkinter.Label(self.root,text="Enter RPM:").pack()
		mentry = Tkinter.Entry(self.root,textvariable=self.speed).pack()
		mbutton = Tkinter.Button(self.root,text='Enter',command=self.mhello,fg='black',bg='grey').pack()
		self.root.bind('<Return>', self.mhello)
		self.root.mainloop()

class SerialData(object):
    def __init__(self, init=50):
        try:
            self.ser = ser = serial.Serial('COM4', 9600)
                #port='com3',
                #baudrate=9600,
                #bytesize=serial.EIGHTBITS,
                #parity=serial.PARITY_NONE,
                #stopbits=serial.STOPBITS_ONE,
                #timeout=0.1,
                #xonxoff=0,
                #rtscts=0,
                #interCharTimeout=None
            #)
        except serial.serialutil.SerialException:
            #no serial connection
            self.ser = None
        else:
            Thread(target=receiving, args=(self.ser,)).start()

    def next(self):
        if not self.ser:
            return 100 #return anything so we can test when Arduino isn't connected
        #return a float value or try a few times until we get one
        for i in range(40):
            raw_line = last_received
            try:
                return float(raw_line.strip())
            except ValueError:
                #print 'bogus data',raw_line
                time.sleep(.005)
        return 0.
    def __del__(self):
        if self.ser:
            self.ser.close()

if __name__=='__main__':
    s = SerialData()
    for i in range(500):
        time.sleep(.015)
        print s.next()
