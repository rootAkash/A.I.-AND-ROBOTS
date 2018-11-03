import serial
import time
ArduinoSerial = serial.Serial('com16',115200)
ArduinoSerial.reset_output_buffer()
time.sleep(2)
print(ArduinoSerial.readline())
count=0
while 1: #Do this forever

     #get input from user
     
    time.sleep(.01)#print the intput for confirmation
    count=count+1
    if(count%2==0):
        var='1'
    else:
        var='2'
      
    if (var == '1'): #if the value is 1
        ArduinoSerial.write(b'1') #send 1
        print ("motor turned ON")
        
    
    if (var == '2'): #if the value is 0
        ArduinoSerial.write(b'0') #send 0
        print ("motor turned OPP")
        
