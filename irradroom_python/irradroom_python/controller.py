import rclpy
import serial
import time, datetime
import pymongo
from bson.json_util import dumps
import bson
from rclpy.node import Node
import sched, time

from std_msgs.msg import String, Int8
from sensor_msgs.msg import Range
from irradroom_cmake.msg import ProgramStatus

from irradroom_cmake.srv import RunProgram

class Controller(Node):

    def __init__(self):
        super().__init__("range_measurer")
        #self.publisher = self.create_publisher(Range, "distance", 10)

        self.mdb = pymongo.MongoClient("mongodb://localhost:27017/").IRRADROOM
        
        self.srv = self.create_service(RunProgram, 'run_program', self.run_program_callback)

        self.pub_program_status = self.create_publisher(ProgramStatus, "program_status", 10)
        self.pub_motor_position = self.create_publisher(String, "source_position_status", 10)
        self.subscription_door_position = self.create_subscription(Int8, "door_status", self.door_position_callback, 10)
        self.pub_motor_cmd = self.create_publisher(String, "motor_cmd", 10)


        self.timer = self.create_timer(0.1, self.loop)
        self.timer2 = self.create_timer(0.5, self.loop_send)
        
        print("Controller spusten")

        self.door = 1 

        self.actual_run = None
        self.actual_info = {}
        self.actual_program = None
        self.actual_step = 0
        self.actual_start = 0
        self.actual_message = ''

        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.logger = self.get_logger()


    def loop(self):
        self.scheduler.run(blocking=False)

    def loop_send(self):
        self.send_program_status()


    def send_program_status(self):
        msg = ProgramStatus()
        run = bool(self.actual_run)
        msg.program_status = int(run)
        msg.message = self.actual_message

        if run:
            msg.run_id = str(self.actual_info.get('name', self.actual_run))
            msg.step = self.actual_step
            msg.start = int(self.actual_start)
            msg.duration = int(time.time() - self.actual_start)
        self.pub_program_status.publish(msg)


    def send_motor_cmd(self, cmd):
        msg = String()
        msg.data = cmd
        self.pub_motor_cmd.publish(msg)

    def do_step(self, job = None, step = None):
        self.logger.info("Do step {}, {}".format(step, job))

        self.actual_step = step+1

        self.send_program_status()

        if job == 'sleep':
            return True

        elif job == 'PosA':
            self.send_motor_cmd('posA')
            print("Move to A")

        elif job == 'PosB':
            self.send_motor_cmd('posB')
            print("Move to B")

        elif job == 'stop':
            self.send_motor_cmd('stop')
            print("Move to A")

        elif job == 'end':
            self.send_motor_cmd('stop')
            #self.actual_run = None
            self.scheduler.enter(20, 1, self.do_step, kwargs={'job': 'end_program', 'step': -1})
            self.actual_message = "Ukončuji program"
            print("Konec!")

        elif job == 'end_program':
            self.actual_run = None
            self.send_motor_cmd('float')
            self.actual_message = ''



    def run_program(self, run_key, run_id):
        program = list(self.mdb.runs.find({'run_key': int(run_key) }))
        if len(program) > 0:
            program = program[0]

        # Iniciovat promenne
        self.actual_run = program['_id']
        self.actual_info = program
        self.actual_program = program['job']
        self.actual_step = 0
        self.actual_start = int(time.time())
        self.actual_message = "Načítám program"

        delay = 0

        # Naplanovat jednotlive kroky programu
        for i, step in enumerate(self.actual_program):
            print(i, "Udelat", step['operation'], "za", delay)
            self.scheduler.enter(delay, 2, self.do_step, kwargs={'job': step['operation'], 'step': i})
            delay += float(step['duration'])

        # Vzdy provest ukonceny
        self.scheduler.enter(delay+1, 1, self.do_step, kwargs={'job': 'end', 'step': len(self.actual_program)+0})
        print(len(self.actual_program), "Udelat", 'end', "za", delay+1)
        
        self.actual_message = "Spuštěn program"

        

    def run_program_callback(self, request, response):
        self.logger.info("CALLBACK - RUN PROGRAM")
        self.logger.info(request.run_id)
        self.logger.info(request.run_key)

        if request.run_id == '' and request.run_key == '':
            self.cancel_program()

            response.start_status = -2
            response.message = "Program cancelled"
            return response
        
        if self.door:    
            response.start_status = -3
            response.message = "Dvere otevreny"
            return response

        if self.actual_run:
            response.start_status = -1
            response.message = "Neco uz bezi"
            return response


        program = list(self.mdb.runs.find({'run_key': int(request.run_key) }))
        if len(program) > 0:
            program = program[0]
        else:
            response.start_status = -4
            response.message = "Prazdny program"
            return response

        # Spustit program
        self.get_logger().info(str(program))
        self.run_program(program['run_key'], program['_id'])

        response.start_status = 1
        response.message = "Spouštím tento program" 
        return response

    # Vymazat vsechny kroky v rade
    def cancel_program(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.do_step('end')

    def door_position_callback(self, msg):
        door = msg.data
        self.door = door

        if door and self.actual_run:
            self.cancel_program()



def main(args=None):
    rclpy.init(args=args)
    rm = Controller()
    rclpy.spin(rm)

    rm.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
