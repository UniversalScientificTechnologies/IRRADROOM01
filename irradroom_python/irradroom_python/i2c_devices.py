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



class I2C_devices(Node):

    def __init__(self):
        super().__init__("i2c_devices")
        self.subscription_dist = self.create_subscription(Range, "distance", self.distance_callback, 10)
        self.i2c_initialized = False
        self.i2c_init()

        timer = 0.5
        self.timer = self.create_timer(timer, self.loop)
        self.i = 0

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


        self.motor = axis.axis_between(SPI = spi, SPI_CS = spi.I2CSPI_SS0, StepsPerUnit=1)
        self.motor.setConfig(F_PWM_INT = None, F_PWM_DEC = None, POW_SR = None, OC_SD = None, RESERVED = None, EN_VSCOMP = None, SW_MODE = None, EXT_CLK = None, OSC_SEL = None)
        self.motor.Setup(MAX_SPEED = 200, KVAL_ACC=0.5, KVAL_RUN=0.5, ACC = 100, DEC = 100, FS_SPD=3000)


        self.motor.setMaxSpeed(speed = 500)
        self.motor.setMinSpeed(speed = 10*16, LSPD_OPT = True)

        n1 = cfg.get_device("pca9635_1")
        n2 = cfg.get_device("pca9635_2")
        n3 = cfg.get_device("pca9635_3")
        n4 = cfg.get_device("pca9635_4")

        time.sleep(0.5)

        self.disp = LED7SEG01A_array([n1, n2, n3, n4])

        self.i2c_initialized = True
        print("I2C init done")


    def distance_callback(self, data):
        self.distance = data.range
        self.distance_update = True
        #print("update_distance", self.distance)
        text = "{}   ".format(int(self.distance))
        print("dist", text)
        if self.i2c_initialized:
            print("write")
            #self.disp.clear_all()
            self.disp.set_text(text+"  ")
            self.motor.GoTo(int(self.distance)*1000)

    def loop(self):
        self.i+= 1
        print("loop", self.i)



def main(args=None):
    rclpy.init(args=args)
    i2c = I2C_devices()
    rclpy.spin(i2c)

    i2c.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


