import datetime
import paho.mqtt.client as mqtt
import time
import serial
import numpy as np
import math

'''
Uses the following installed via pip3:
	numpy
	pyserial
	paho-mqtt
'''

# Talk to the OpenScale board...
ser = serial.Serial(
	port = '/dev/ttyS0',
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1)

def weigh():
	print("weighing...")
	# Take one minute of samples
	endTime = datetime.datetime.now() + datetime.timedelta(minutes=1)
	readings = []
	while True:
		if datetime.datetime.now() >= endTime:
			break
		reading = ser.readline()
		if len(reading.decode('UTF-8')) > 0:
			data = reading.decode('UTF-8').replace('\n', '').replace('\r', '')
			# The data we get from openscale is in the format: "589840246,4.89,lbs,23.75,0,"
			# where the weight is position 1 in the array
			dataparts = data.split(',')
			readings.append(dataparts[1])

	# And return the mean of the samples
	return math.floor(np.mean(np.array(readings).astype(np.float)))

while True:
	weight = weigh()
	ts = round(time.time())
	txline = str(ts) + "," + str(weight)
	now = datetime.datetime.now()
	print (now.strftime("%Y-%m-%d %H:%M:%S"))
	print("Current weight is " + str(weight))
	# Set up our mqtt connection
	try:
		client = mqtt.Client()
		client.connect('glue', 1883, 60)
		client.publish('propanescaletopic', txline)
		client.disconnect()
	except:
		print("Had an error connecting to glue")

