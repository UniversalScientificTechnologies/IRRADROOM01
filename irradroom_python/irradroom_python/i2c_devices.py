import rclpy
import serial
import time
from rclpy.node import Node

import time
import datetime
import sys
from pymlab import config
from pymlab.helpers.LED7SEG01A_array import LED7SEG01A_array
import axis


from std_msgs.msg import String
from sensor_msgs.msg import Range

steps = 100*18


class I2C_devices(Node):

    def __init__(self):
        super().__init__("i2c_devices")
        self.subscription_dist = self.create_subscription(Range, "distance", self.distance_callback, 10)
        self.subscription_source_position = self.create_subscription(Range, "source_position", self.source_position_callback, 10)
        self.subscription_motor_position = self.create_subscription(String, "motor_cmd", self.motor_position_callback, 10)
        self.i2c_initialized = False
        self.motor_position_valid = False
        self.motor_communication = True

        self.i2c_init()

        timer = 0.5
        self.timer = self.create_timer(timer, self.loop)
        self.i = 0

        self.declare_parameter('source_position_min', 25)
        self.declare_parameter('source_position_max', 25+150)
        self.declare_parameter('source_position_center', 15+150/2)
        self.declare_parameter('source_position_A', 25+20)
        self.declare_parameter('source_position_B', 25+150-20)

        #self = self.get_parameter('my_str')

        self.distance = 0
        self.distance_update = False

    def i2c_init(self):

        port = 1
        cfg = config.Config(
            i2c = {
                "port": port,
            },
            bus = [
                {
                "type": "i2chub",
                "address": 0x70,

                "children": [
                    {"name": "pca9635_1", "type": "PCA9635", "channel": 0},
                    {"name": "pca9635_2", "type": "PCA9635", "channel": 1},
                    {"name": "pca9635_3", "type": "PCA9635", "channel": 2},
                    {"name": "pca9635_4", "type": "PCA9635", "channel": 3},
                ],
                },
                {
                    "name":"spi",
                    "type":"i2cspi"
                },

            ],
        )
        cfg.initialize()

        spi = cfg.get_device("spi")
        spi.SPI_config(spi.I2CSPI_MSB_FIRST| spi.I2CSPI_MODE_CLK_IDLE_HIGH_DATA_EDGE_TRAILING |spi.I2CSPI_CLK_461kHz)


        self.motor = axis.axis(SPI = spi, SPI_CS = spi.I2CSPI_SS0, StepsPerUnit=1)
        self.motor.setConfig(F_PWM_INT = None, F_PWM_DEC = None, POW_SR = None, OC_SD = None, RESERVED = None, EN_VSCOMP = None, SW_MODE = None, EXT_CLK = None, OSC_SEL = None)
        self.motor.Setup(MAX_SPEED = 200, KVAL_ACC=0.3, KVAL_RUN=0.3, KVAL_DEC=0.3, ACC = 100, DEC = 100, FS_SPD=3000)


        self.motor.setMaxSpeed(speed = 300)
        self.motor.setMinSpeed(speed = 10*16, LSPD_OPT = True)

        n1 = cfg.get_device("pca9635_1")
        n2 = cfg.get_device("pca9635_2")
        n3 = cfg.get_device("pca9635_3")
        n4 = cfg.get_device("pca9635_4")

        time.sleep(0.5)

        self.disp = LED7SEG01A_array([n1, n2, n3, n4])

        self.i2c_initialized = True
        print("I2C init done")

        #self.motor.GoTo(int(200*8*50))
        #self.motor.Move(-50*100, direction = 0)
        self.motor_communication = False
        # print("......")
        # time.sleep(50)
        # print("END")
        # self.motor.Float()


    def distance_callback(self, data):
        self.distance = data.range
        self.distance_update = True
        #print("update_distance", self.distance)
        text = "{}   ".format(int(self.distance))
        print("dist", text)
        #if self.i2c_initialized:
        #    print("write")
        #    #self.disp.clear_all()
        #    self.disp.set_text(text+"  ")

    def source_position_callback(self, data):

        if self.i2c_initialized and not self.motor_position_valid:
            self.motor.Float()
            time.sleep(1)
            print("Nastavuji polohu motoru ze senzoru: {}mm -> {}units".format(data.range, data.range*50*100))
            self.motor.setPosition(steps*data.range)
            self.motor_position_valid = True

    def motor_position_callback(self, data):
        print("data", data)
        d = data.data
        if "posA" in d:
            self.motor.GoTo((25+20)*steps)
        elif "posB" in d:
            self.motor.GoTo((25+150-20)*steps)
        elif "stop" in d:
            self.motor.GoTo((25+150/2)*steps)
        elif "float" in d:
            self.motor.Float()

    def loop(self):
        self.i+= 1
        print("loop", self.i)
        if not self.motor_communication:
            status = self.motor.getStatus()
            print(status)
            print("Position>>>", status.get('POSITION', 0)/(steps))


def main(args=None):
    rclpy.init(args=args)
    i2c = I2C_devices()
    rclpy.spin(i2c)

    i2c.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
