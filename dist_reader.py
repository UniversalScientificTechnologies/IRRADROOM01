import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 19200)


def read_data(parametr):
	if parametr == "dist":
		ser.write('D')
		data = ser.readline().rstrip('\n\r')
		data_split = data.split(",")
		dist = data_split[0][3:-1]
		return dist
	elif parametr == "temp":
		ser.write('S')
		data = ser.readline().rstrip('\n\r')
		data_split = data.split(",")
		temp = data_split[0][3:-2]
		return temp
	elif parametr == "volt":
		ser.write('S')
		data = ser.readline().rstrip('\n\r')
		data_split = data.split(",")
		volt = data_split[1][0:-1]
		return volt

while True:
	dist = read_data("dist"), read_data("temp"), read_data("volt")
	print (dist)
	#print ("distance = %sm") %(distance)
	time.sleep(10)

