#!/usr/bin/env python3
#############################################################################
# Filename : DHT11.py Description : read the temperature and humidity data of DHT11 Author : freenove modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT
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
        f = open('TempOut.txt', 'w')
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
                                        f.write(rollingavgtem)
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
                time.sleep(3)
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        f.close()
        GPIO.cleanup()
        exit()
