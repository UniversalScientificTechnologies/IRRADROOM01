import rclpy
import serial
import time
from rclpy.node import Node

from std_msgs.msg import Int8
import odroid_wiringpi as wpi

class DoorStatus(Node):

    def __init__(self):
        super().__init__("door_status")
        self.publisher = self.create_publisher(Int8, "door_status", 10)
        timer = 0.5

        wpi.wiringPiSetup()
        wpi.pinMode(27, 0)
        wpi.pullUpDnControl(27, 2)
        self.timer = self.create_timer(timer, self.measure)
        self.i = 0


    def measure(self):
        try:
            msg = Int8()
            msg.data = wpi.digitalRead(27)
            print("status:", msg.data)
            self.publisher.publish(msg)
        except Exception as e:
            print(e)

def main(args=None):
    rclpy.init(args=args)
    sp = DoorStatus()
    rclpy.spin(sp)

    sp.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
