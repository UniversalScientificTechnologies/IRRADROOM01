import rclpy
import serial
import time
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Range



class RangeMeasure(Node):

    def __init__(self):
        super().__init__("range_measurer")
        self.publisher = self.create_publisher(Range, "distance", 10)
        self.ser = serial.Serial('/dev/ttyS1', 19200)
        timer = 0.5
        self.timer = self.create_timer(timer, self.measure)
        self.i = 0

    def read_data(self, parametr):
        if parametr == "dist":
            self.ser.write(b'D')
            data = str(self.ser.readline()).rstrip('\n\r')
            data_split = data.split(",")
            dist = float(data_split[0][4:-1])*100.0
            return dist

        elif parametr == "temp":
            self.ser.write(b'S')
            data = str(self.ser.readline()).rstrip('\n\r')
            data_split = data.split(",")
            temp = float(data_split[0][4:-2])
            return temp

        elif parametr == "volt":
            self.ser.write(b'S')
            data = str(self.ser.readline()).rstrip('\n\r')
            data_split = data.split(",")
            volt = data_split[1][0:-1]
            return volt


    def measure(self):
        try:
            msg = Range()
            msg.range = self.read_data("dist")
            print("distance:", msg.range)
            self.publisher.publish(msg)
            self.i += 1
        except Exception as e:
            print(e)

def main(args=None):
    rclpy.init(args=args)
    rm = RangeMeasure()
    rclpy.spin(rm)

    rm.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
