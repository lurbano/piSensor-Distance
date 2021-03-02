#!/usr/bin/python
# for sensor HC-SRO4
import RPi.GPIO as GPIO
import time
import json
import asyncio

class sensor_D:

    def __init__(self, server, pin_trigger = 23, pin_echo = 24):
        GPIO.setmode(GPIO.BCM)
        self.PIN_TRIGGER = pin_trigger
        self.PIN_ECHO = pin_echo
        GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(self.PIN_ECHO, GPIO.IN)

        self.server = server
        self.log = []
        self.task = None
        self.taskType = None

    def cancelTask(self):
        print("Canceling last task.")
        if self.task:
            self.task.cancel()
            self.taskType = None

    async def async_measure(self, returnType='none'):
        d = self.measure(returnType)
        #print(f"measured async:{d}")
        return d

    def measure(self, returnType='none'):
        # set returnType to 'json' to return json formatted text.
        #GPIO.output(self.PIN_TRIGGER, GPIO.LOW)
        # print( "Waiting for sensor to settle")
        #time.sleep(0.1)
        #print ("Calculating distance")

        GPIO.output(self.PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)

        # pulse_start_time = 0
        # pulse_end_time = 0

        while GPIO.input(self.PIN_ECHO)==0:
            pulse_start_time = time.time()
        while GPIO.input(self.PIN_ECHO)==1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        pulseTime = (pulse_end_time - pulse_start_time) / 2
        #print ("Distance:",distance,"cm")
        if returnType == 'json':
            d = {
                "sensor" : 'HC-SRO4',
                'measurement': 'distance',
                'units': "cm",
                "data": distance,
                "time": pulseTime
                }
            return(d)
        elif returnType == 'tdt':
            t = pulse_end_time - (pulse_duration/2)
            d = (t, distance)
            return d
        else:
            return distance

    async def aRead(self, getTime=False, log=False, update="live"):
        # print("measuring...")
        measurement = self.measure("json")
        # print("measurement = ")
        # print(measurement)
        # print(measurement["data"])

        message = {}
        message["S"] = measurement["data"]
        message["units"] = measurement["units"]

        if getTime:
            message["t"] = time.ctime(time.time())
        if log:
            m = {"x": T_C, "t":round(time.time()-self.startTime, 4)}
            self.log.append(m)
            if update == "live":
                m['timeLeft'] = self.timeLeft
                m["info"] = "logUp"
                self.server.write_message(m)
        message["info"] = "S-one"
        self.server.write_message(message)
        return message

    async def aMonitor(self, dt):
        self.taskType = "monitor"
        print("monitor: dt=", dt)
        while 1:
            await asyncio.gather(
                asyncio.sleep(dt),
                self.aRead( True, False, 'live')
            )

    async def aLedStrip(self, ledPix, dt, ledMaxRange, ledMinRange):
        self.taskType = "led"
        print(f"Working LEDs: {ledPix.nPix}")
        while 1:
            dist = self.measure()
            n = int(ledPix.nPix * (dist - ledMinRange) / (ledMaxRange-ledMinRange))
            print(f"dist: {dist}, n: {n}")
            ledPix.twoColors(n)
            await asyncio.sleep(dt)



    def multipulse(self, nPulses=10):
        data = []
        for i in range(nPulses):
            data.append(self.measure())
        print(data)

        # screen for outliers (over 2000 cm)
        tot = 0
        n = 0
        for i in data:
            if i < 2000:
                tot += i
                n += 1
        if n > 0:
            avg = tot/n
        else:
            avg = 0.0   #divide by zero error
        return avg

    def log(self, dt, tt):
        for t in range(10): #for t in arange(0, tt+dt, dt):
            print(t)
            sleep(dt)
        return ("logged!")

    async def async_log(self, dt, tt):
        data = []
        for i in arange(0.0, tt+dt, dt):
            nxt = tornado.gen.sleep(dt)
            d = await self.async_measure()
            data.append([i,d])
            await nxt
        return data




    def cleanup(self):
        GPIO.cleanup()

class LogDistanceData:

    def __init__(self, dt=1.0):
        self.log_start_time = time.time()
        self.dt = dt
        l_loop = True
