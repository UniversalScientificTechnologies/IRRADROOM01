import rclpy
import serial
import time
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Range



class SourcePosition(Node):

    def __init__(self):
        super().__init__("source_position")
        self.publisher = self.create_publisher(Range, "source_position", 10)
        self.ser = serial.Serial('/dev/ttyS2', 9600)
        timer = 0.5
        self.timer = self.create_timer(timer, self.measure)
        self.i = 0

    def pack(self, val):
        print(hex(0xA5), hex(val), hex(val+0xA5))
        ar = bytearray([0xA5, val, 0xA5+val])
        print(ar)
        return ar


    def read(self):
        loop = 0
        pos = 1
        ar = []
        self.ser.read_all()
        for i in range(15):
            ch = self.ser.read()
            if ch == b'Z' and pos:
                if pos > 5 and ar[0] == b'Z' and ar[1] == b'Z':
                    break
                pos = 0
                ar = [ch]
                continue
            elif ch == b'Z' and not pos:
                pos += 1
                ar += [ch]
            else:
                pos += 1
                ar += [ch]
        #print(ar)
        return float(ord(ar[4]) << 8 | ord(ar[5]))


    def measure(self):
        try:
            msg = Range()
            msg.range = self.read()
            msg.min_range = 15.0
            msg.max_range = 150.0
            print("distance:", msg.range)
            self.publisher.publish(msg)
            self.i += 1
        except Exception as e:
            print(e)

def main(args=None):
    rclpy.init(args=args)
    sp = SourcePosition()
    rclpy.spin(sp)

    sp.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
