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
from std_msgs.msg import Int8
from sensor_msgs.msg import Range

from threading import Lock

steps = 100*18


class I2C_devices(Node):

    def __init__(self):
        super().__init__("i2c_devices")
        self.subscription_dist = self.create_subscription(Range, "distance", self.distance_callback, 10)
        self.subscription_source_position = self.create_subscription(Range, "source_position", self.source_position_callback, 10)
        self.subscription_motor_position = self.create_subscription(String, "motor_cmd", self.motor_position_callback, 10)
        self.subscription_door_position = self.create_subscription(Int8, "door_status", self.door_position_callback, 10)

        self.publisher = self.create_publisher(Int8, "source_position_status", 10)

        self.i2c_initialized = False
        self.motor_position_valid = False
        self.motor_communication = True

        self.logger = self.get_logger()

        self.i2c_lock = Lock()

        self.i2c_init()

        timer = 1
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
        self.last_door = 1

    def i2c_init(self):

        self.i2c_lock.acquire()

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
        self.motor.Setup(MAX_SPEED = 500, KVAL_ACC=0.8, KVAL_RUN=0.9, KVAL_DEC=0.8, ACC = 500, DEC = 2000, FS_SPD=3000, STEP_MODE=axis.axis.STEP_MODE_1_16)


        self.motor.setMaxSpeed(speed = 300+200)
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
        self.i2c_lock.release()



    def distance_callback(self, data):
        self.distance = data.range
        self.distance_update = True
        #print("update_distance", self.distance)
        text = "{}   ".format(int(self.distance))
        print("dist", text)
        if self.i2c_initialized:
            self.i2c_lock.acquire()
            self.disp.set_text(text+"  ")
            self.i2c_lock.release()

    def source_position_callback(self, data):

        print("source position", data.range)
        if data.range < 80:
            self.send_source_position(-1)
        elif data.range > 120:
            self.send_source_position(1)
        else:
            self.send_source_position(0)


        if self.i2c_initialized and not self.motor_position_valid:
            self.i2c_lock.acquire()
            
            self.motor.Float()
            time.sleep(1)
            print("Nastavuji polohu motoru ze senzoru: {}mm -> {}units".format(data.range, data.range*50*100))
            self.motor.setPosition(steps*data.range)
            self.motor_position_valid = True

            self.i2c_lock.release()

            self.move_motor('stop')


    def door_position_callback(self, data):
        current_door = data.data
        print("Dvere", current_door)
        if not self.last_door and current_door:
            print("Dvere otevrene")
            #if self.i2c_initialized and not self.motor_position_valid:
            self.last_door = current_door
            self.move_motor("stop")

        if self.last_door != current_door:
            self.last_door = current_door
    
    def send_source_position(self, position):
        msg = Int8()
        msg.data = int(position)
        print(int(position), msg)
        self.publisher.publish(msg)


    def move_motor(self, pos):
        print("Move motor", pos)
        if pos == "posA":
            self.i2c_lock.acquire()
            print("Posouvam motor na A")
            self.motor.Float()
            self.motor.Wait()
            self.motor.GoTo((25+20)*steps)
            self.i2c_lock.release()
            #self.send_source_position(-1)

        elif pos == "posB":
            self.i2c_lock.acquire()
            print("Posouvam motor na B")
            self.motor.Float()
            self.motor.Wait()
            self.motor.GoTo((25+150-20)*steps)
            self.i2c_lock.release()
            #self.send_source_position(1)

        elif pos == "stop":
            self.i2c_lock.acquire()
            print("Posouvam motor DOMU")
            self.motor.Float()
            self.motor.Wait()
            self.motor.GoTo((25+150/2)*steps)
            self.i2c_lock.release()
            #self.send_source_position(-1)

        elif pos == "float":
            self.i2c_lock.acquire()
            print("Vypinam motor")
            self.motor.Float()
            self.i2c_lock.release()
        
        print("pozice nastavena ")
        self.last_motor_operation = time.time()
    

    def motor_position_callback(self, data):
        d = data.data
        self.logger.info("MotorPositionCallback: {}".format(d))

        d = data.data
        if "posA" in d:
            print(d, "<<<")
            self.move_motor("posA")
        elif "posB" in d:
            print(d, "<<<")
            self.move_motor("posB")
        elif "stop" in d:
            print(d, "<<<")
            self.move_motor("stop")
        elif "float" in d:
            print(d, "<<<")
            self.move_motor("float")

    def loop(self):
        self.i2c_lock.acquire()
        status = self.motor.getStatus()
        #print(status)
        #print("Position HBSTEP>>>", status.get('POSITION', 0)/(steps))
        self.i2c_lock.release()
        #self.send_source_position()


def main(args=None):
    rclpy.init(args=args)
    i2c = I2C_devices()
    rclpy.spin(i2c)

    i2c.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
