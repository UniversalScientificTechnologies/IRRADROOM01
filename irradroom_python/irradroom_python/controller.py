import rclpy
import serial
import time
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Range



class Controller(Node):

    def __init__(self):
        super().__init__("range_measurer")
        #self.publisher = self.create_publisher(Range, "distance", 10)

        timer = 0.5
        self.timer = self.create_timer(timer, self.loop)
        self.i = 0

    def loop(self):
        pass

def main(args=None):
    rclpy.init(args=args)
    rm = Controller()
    rclpy.spin(rm)

    rm.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
