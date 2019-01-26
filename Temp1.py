#!/usr/bin/env python3
#############################################################################
# Filename : DHT11.py Description : read the temperature and humidity data of DHT11 Author : freenove modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT
DHTPin = 11 #define the pin of DHT11

def loop():
        dht = DHT.DHT(DHTPin) #create a DHT class object
        sumCnt = 0 #number of reading times
        fieldfill = 0
        templist = []
        humidlist = []
        rollingavghum = 0
        rollingavgtem = 0
        while(True):
                sumCnt += 1 #counting number of reading times
                chk = dht.readDHT11() #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
                print "**********************************************************************"
                print ("The sumCnt is : %d, \t chk : %d"%(sumCnt,chk))
                if (chk is dht.DHTLIB_OK): #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
                        print("DHT11,OK!")
                        if (fieldfill < 11):
                                templist.append(dht.temperature)
                                humidlist.append(dht.humidity)
                                fieldfill +=1
                        else:
                                templist[0] = templist[1]
                                humidlist[0] = humidlist[1]
                                templist[1] = templist[2]
                                humidlist[1] = humidlist[2]
                                templist[2] = templist[3]
                                humidlist[2] = humidlist[3]
                                templist[3] = templist[4]
                                humidlist[3] = humidlist[4]
                                templist[4] = templist[5]
                                humidlist[4] = humidlist[5]
                                templist[5] = templist[6]
                                humidlist[5] = humidlist[6]
                                templist[6] = templist[7]
                                humidlist[6] = humidlist[7]
                                templist[7] = templist[8]
                                humidlist[7] = humidlist[8]
                                templist[8] = templist[9]
                                humidlist[8] = humidlist[9]
                                templist[9] = templist[10]
                                humidlist[9] = humidlist[10]
                                templist[10] = dht.temperature
                                humidlist[10] = dht.humidity
                                rollingavgtem = 0
                                rollingavghum = 0
                                for i in range(0, fieldfill):
                                        rollingavgtem += templist[i]
                                        rollingavghum += humidlist[i]
                                rollingavgtem = round((rollingavgtem / fieldfill), 2)
                                rollingavghum = round((rollingavghum / fieldfill), 2)
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
        GPIO.cleanup()
        exit()
