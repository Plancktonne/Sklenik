#!/usr/bin/env python3
#############################################################################
# Filename : DHT11.py Description : read the temperature and humidity data of DHT11 Author : freenove modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT

from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
#from RPLCD import CharLCD


#INI phase
GPIO.cleanup() #safety cleanup
DHTPin = 11 #define the pin of DHT11 11=GPIO17
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.



def loop():                     #Main Loop
        dht = DHT.DHT(DHTPin) #create a DHT class object
        sumCnt = 0 #number of reading times
        fieldfill = 0 #integer for measuring field fullnes
        templist = [] #field for temperatures
        humidlist = [] #field for humidity
        rollingavghum = 0 #average huimidity value from last 10 valid measurements
        rollingavgtem = 0 #average temperature value from last 10 valid measurements
        mcp.output(3,1)     # turn on LCD backlight
        lcd.begin(16,2)     # set number of LCD lines and columns



        while(True):
                sumCnt += 1 #counting number of reading times
                chk = dht.readDHT11() #read DHT11 and get a return value.
                print ("**********************************************************************")
                print ("The sumCnt is : %d, \t chk : %d"%(sumCnt,chk)) #print number of measurements and current return value from DHT sensor
                if (chk is dht.DHTLIB_OK): #determine whether data read is normal according to the return value.
                        print("DHT11,OK!") #return value ok
                        if (fieldfill < 11): #filling of the field
                                if ((dht.temperature < 100) and (dht.humidity < 100)): #check if temp and humidity are inside valid range
                                    templist.append(dht.temperature) 
                                    humidlist.append(dht.humidity) 
                                    fieldfill +=1
                        else:                   #field alredy full, start overwriting
                                if ((dht.temperature < 100) and (dht.humidity < 100)):  #check if temp and humidity are inside valid range
                                    for i in range(0, fieldfill-1):
                                        templist[i] = templist[i+1]
                                        humidlist[i] = humidlist[i+1]                             
                                    templist[10] = dht.temperature
                                    humidlist[10] = dht.humidity
                                    rollingavgtem = 0
                                    rollingavghum = 0
                                    for i in range(0, fieldfill):
                                            rollingavgtem += templist[i]
                                            rollingavghum += humidlist[i]
                                    rollingavgtem = round((rollingavgtem / fieldfill), 2)
                                    rollingavghum = round((rollingavghum / fieldfill), 2)
                                    if ((rollingavgtem != 0) or (rollingavghum != 0)):
                                        TempIO.write("%.2f, "%(rollingavgtem)) #write to temp log
                                        HumIO.write("%.2f, "%(rollingavghum)) #write to humid log
                                        localtime = time.localtime(time.time()) #get current time
                                        TimeIO.write("%i:%i:%i,"%(localtime.tm_hour, localtime.tm_min, localtime.tm_sec)) #write to time log 
#
# DHT Read ERRORS
#
                elif(chk is dht.DHTLIB_ERROR_CHECKSUM): #data check has errors
                        print("DHTLIB_ERROR_CHECKSUM!!")
                elif(chk is dht.DHTLIB_ERROR_TIMEOUT): #reading DHT times out
                        print("DHTLIB_ERROR_TIMEOUT!")
                else: #other errors
                        print("Other error!")
#

#
#Printing of results
#
                print("Humidity: %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))
                print("Field of Temperatures: ")
                print(templist)
                print("RollingAVG Temperature: %.2f \n"%(rollingavgtem))
                print("Field of Humidities: ")
                print(humidlist)
                print("RollingAVG Humidity: %.2f \n"%(rollingavghum))
#
#LCD refresh
#
                lcd.clear() #clear current message
                lcd.setCursor(0,0)  # reset cursor position
                lcd.message( 'Tempera.: %0.2f\nHumidity: %0.2f' %(rollingavgtem,rollingavghum))  # display averages
#
##irrigation part
#
GPIO.output(36, GPIO.HIGH)
sleep(2)
GPIO.output(36, GPIO.LOW)
#
#
                time.sleep(10) #wait 10s between measurements
             

def destroy():

    lcd.clear()


# Create PCF8574 GPIO adapter.
try:
	mcp = PCF8574_GPIO(PCF8574A_address)
except:
	try:
		mcp = PCF8574_GPIO(PCF8574_address)
	except:
		print ('I2C Address Error !')
		exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Program is starting ... ')
    TempIO = open('TempOut.txt', 'w')
    HumIO = open('HumOut.txt', 'w')
    TimeIO = open('TimeOut.txt', 'w')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        TempIO.close()
        HumIO.close()
        TimeIO.close()
        GPIO.cleanup()
        exit()
