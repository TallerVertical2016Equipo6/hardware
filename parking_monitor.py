import sys
import time
import pyupm_grove as grove
import pyupm_i2clcd as lcd
from socketIO_client import SocketIO, BaseNamespace

class SensorNamespace(BaseNamespace):
    def on_connect(self):
        print('[Connected]')

# Function to initialize global variables
def on_signal(*args):
    global available
    global capacity
    available = args[0]['availability']
    capacity = args[0]['capacity']                                             

# Create the socketIO connection                                               
socketIO = SocketIO('antoniohernandez.me', 8000)
sensor_socket = socketIO.define(SensorNamespace, '/sensor')
sensor_socket.emit('initialize', {'area': sys.argv[1]})
sensor_socket.on('initialize', on_signal)
socketIO.wait(seconds=2)

# Create the buttons
buttonInp = grove.GroveButton(8)
buttonInp2 = grove.GroveButton(2)
buttonOut = grove.GroveButton(5)
buttonOut2 = grove.GroveButton(4)
flag=True
# Initialize Jhd1313m1 at 0x3E (Lcd address)
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)                                           
                                                                               
# Waiting 0.5 second between readings
while 1:

    # Change color of the LCD
    if available >= capacity *.3:
        myLcd.setColor(0, 255, 10)

    if available > 0 and available < capacity*.3:
        myLcd.setColor(255, 55, 0)

    if available == 0:
        myLcd.setColor(255, 0, 0)

    #Change the value of available variable
    if buttonInp.value() == 1:
        available= available - 1
        if available < 0:
            sensor_socket.emit('signal', {'area' : sys.argv[1], 'availability' : 0,'capacity' : capacity })
        else:
            sensor_socket.emit('signal', {'area' : sys.argv[1], 'availability' : available,'capacity' : capacity })
        flag=True
    if buttonInp2.value() == 1:
        available= available - 1
        if available < 0:
            sensor_socket.emit('signal', {'area' : sys.argv[1], 'availability' : 0,'capacity' : capacity })
        else:
            sensor_socket.emit('signal', {'area' : sys.argv[1], 'availability' : available,'capacity' : capacity })
        flag=True
    if buttonOut.value() == 1:
        available=available + 1
        if available < 0:
            sensor_socket.emit('signal', {'area' : sys.argv[1], 'availability' : 0,'capacity' : capacity })
        else:
            sensor_socket.emit('signal', {'area' : sys.argv[1], 'availability' : available,'capacity' : capacity })
        flag=True
    if buttonOut2.value() == 1:
        available=available + 1
        if available < 0:
            sensor_socket.emit('signal', {'area' : sys.argv[1], 'availability' : 0,'capacity' : capacity })
        else:
            sensor_socket.emit('signal', {'area' : sys.argv[1], 'availability' : available,'capacity' : capacity })
        flag=True

    # Print LCD
    if flag:                                                                   
        myLcd.setCursor(1,6)
        if available < 0:
            myLcd.write('0')
        else:
            if available<10:
               myLcd.write('0')                                               
            if available<100 and available>9:
                myLcd.setCursor(1,8)
                myLcd.write(' ')
                myLcd.setCursor(1,6)
            myLcd.write(str(available))
        myLcd.setCursor(0,0)
        myLcd.write('Disponibles:')
        myLcd.setCursor(1,0)
        myLcd.write('Zona'+sys.argv[1])
        myLcd.setCursor(1,9)
        myLcd.write('Lugares')
        flag=False
    time.sleep(.5)

# Delete the button object
del buttonInp
del buttonInp2
del buttonOut
del buttonOut2

                     
