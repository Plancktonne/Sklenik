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

GPIO.cleanup()
DHTPin = 11 #define the pin of DHT11

def loop():
        dht = DHT.DHT(DHTPin) #create a DHT class object
        sumCnt = 0 #number of reading times
        fieldfill = 0
        templist = []
        humidlist = []
        rollingavghum = 0
        rollingavgtem = 0
        mcp.output(3,1)     # turn on LCD backlight
        lcd.begin(16,2)     # set number of LCD lines and columns
        #lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])


        while(True):
                sumCnt += 1 #counting number of reading times
                chk = dht.readDHT11() #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
                print ("**********************************************************************")
                print ("The sumCnt is : %d, \t chk : %d"%(sumCnt,chk))
                if (chk is dht.DHTLIB_OK): #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
                        print("DHT11,OK!")
                        if (fieldfill < 11):
                                if ((dht.temperature < 100) and (dht.humidity < 100)):
                                    templist.append(dht.temperature)
                                    humidlist.append(dht.humidity)
                                    fieldfill +=1
                        else:
                                if ((dht.temperature < 100) and (dht.humidity < 100)):
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
                                        TempIO.write("%.2f, "%(rollingavgtem))
                                        HumIO.write("%.2f, "%(rollingavghum))
                                        localtime = time.localtime(time.time())
                                        TimeIO.write("%i:%i:%i,"%(localtime.tm_hour, localtime.tm_min, localtime.tm_sec))

                elif(chk is dht.DHTLIB_ERROR_CHECKSUM): #data check has errors
                        print("DHTLIB_ERROR_CHECKSUM!!")
                elif(chk is dht.DHTLIB_ERROR_TIMEOUT): #reading DHT times out
                        print("DHTLIB_ERROR_TIMEOUT!")
                else: #other errors
                        print("Other error!")

                print("Humidity: %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))
                print("Field of Temperatures: ")
                print(templist)
                print("RollingAVG Temperature: %.2f \n"%(rollingavgtem))
                print("Field of Humidities: ")
                print(humidlist)
                print("RollingAVG Humidity: %.2f \n"%(rollingavghum))

                lcd.clear()
                lcd.setCursor(0,0)  # set cursor position
                lcd.message( 'Tempera.: %0.2f\nHumidity: %0.2f' %(rollingavgtem,rollingavghum))  # display averages
                time.sleep(3)

def destroy():

    lcd.clear()

PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
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
