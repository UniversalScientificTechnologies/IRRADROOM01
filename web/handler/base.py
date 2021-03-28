#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.escape
import tornado.web

import glob
import json
import io
import subprocess
import sqlite3
import time, datetime
import os, sys
import glob
import random


'''


MongoDB seznam databazi:



programs


runs


users

'''


#import rosparam
import hashlib
import pymongo
from bson.json_util import dumps
import bson

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    return d

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        print("Prihlasen", user_json)
        
        if user_json:
            users = list(self.mdb.users.find({"user": user_json.decode("utf-8") }))

            if len(users) > 0:
                return users[0]     

        return None


    def initialize(self):
        self.mdb = pymongo.MongoClient("mongodb://localhost:27017/").IRRADROOM
        
        #self.config = self.settings['']
        #self.db = self.settings['']
        pass

    def get_login_url(self):
        return u"/login"

class Controller(BaseHandler):
    def get(self):
        print("Controller")
        self.render("controller.hbs")

class Controller_get_programs(BaseHandler):
    def get(self):

        mdb = pymongo.MongoClient("mongodb://localhost:27017/").IRRADROOM
        programs = mdb.programs.find({}).sort([('_id', -1)])
        programs = list(programs)

        print(programs)
        self.write(dumps(programs))


class Controller_get_jobs(BaseHandler):
    def get(self):

        mdb = pymongo.MongoClient("mongodb://localhost:27017/").IRRADROOM
        jobs = mdb.runs.find({'run_author': self.current_user.get('user')}).sort([('_id', -1)])
        jobs = list(jobs)

        print(jobs)
        self.write(dumps(jobs))

class Controller_remove_program_step(BaseHandler):
    def get(self, program, step):

        program_id = bson.ObjectId(program)
        mdb = pymongo.MongoClient("mongodb://localhost:27017/").IRRADROOM

        mdb.programs.update({'_id': program_id}, {"$unset" : {"job."+step : 1 }})
        mdb.programs.update({'_id': program_id}, {"$pull" : {"job" : None}})

        self.write("removed")


class Controller_get_program(BaseHandler):
    def get(self, prog_id):
        self.set_header("Content-Type", "application/json")


        mdb = pymongo.MongoClient("mongodb://localhost:27017/").IRRADROOM
        programs = mdb.programs.find({'_id': bson.ObjectId(prog_id)})

        programs = list(programs)[0]

        print(programs)
        self.write(dumps(programs))


class Controller_queue_program(BaseHandler):
    def get(self, prog_id):
        self.set_header("Content-Type", "application/json")

        mdb = pymongo.MongoClient("mongodb://localhost:27017/").IRRADROOM
        program = mdb.programs.find({'_id': bson.ObjectId(prog_id)})
        
        program = list(program)[0]
        program['_id'] = bson.ObjectId()
        program['run_key'] = random.randint(1000,9999)
        program['added'] = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        program['state'] = 0
        program['status'] = 'new'
        program['job_recod'] = []
        program['run_author'] = self.current_user.get('user')

        print(program)
        print(program['job'])

        mdb.runs.insert_one(program)
        self.write(dumps(program))


class Controller_create_program(BaseHandler):
    def get(self):

        pid = bson.ObjectId()

        data = {
            '_id': pid,
            'job': [],
            'description': '',
            'created': datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S"),
            'name': 'Nový program',
            'author_system': self.current_user.get('user'),
            'author_name': self.current_user.get('user')
        }

        mdb = pymongo.MongoClient("mongodb://localhost:27017/").IRRADROOM
        programs = mdb.programs.insert_one(data)

        data = {"program_id": str(pid)}
        self.write(data)

class Controller_edit_program(BaseHandler):
    def get(self, program, step):

        self.set_header("Content-Type", "application/json")
        print("program", program)

        step_data = {
            "operation": self.get_argument('step_operation', 'sleep'),
            "duration": self.get_argument('step_duration', 0)
        }


        mdb = pymongo.MongoClient("mongodb://localhost:27017/").IRRADROOM
        programs = mdb.programs.update({'_id': bson.ObjectId(program)},     
            {"$push": { "job": { "$each": [step_data], "$position": 3 } }}
        )


        # with open('/data/prog/{}.json'.format(program), 'r+') as f:
        #     data = json.load(f)
        #     if not 'job' in data:
        #         data['job'] = []

        #     data['job'].insert(int(step), step_data)

        #     f.seek(0)
        #     json.dump(data, f, indent=4)
        #     f.truncate()
        #     f.close()

        self.write(json.dumps(step_data))

class State(BaseHandler):
    def get(self):
        print("State")
        self.render("state.hbs")


class NodeStart(BaseHandler):
    def get(self, node):
        print(node)
        if self.current_user:
            cmd = ['rosrun', 'arom', node, '&']
            r = subprocess.Popen(cmd)
            return self.write(" - ".join(cmd))
        else:
            return self.write("UserErr")

class PowerOff(BaseHandler):
    def get(self, name=None):
        if self.current_user:
            cmd = ['poweroff']
            r = subprocess.Popen(cmd)
            return self.write(" - ".join(cmd))
        else:
            return self.write("UserErr, zkuste se prihlasit")


class NodeKill(BaseHandler):
    def get(self, node):
        print("KILL",  node)
        if self.current_user:
            cmd = ['rosnode', 'kill', '/'+node]
            r = subprocess.call(cmd)
            return self.write(repr(cmd))
        else:
            return self.write("UserErr")

class GetImage(BaseHandler):
    def get(self, node):
        print("GetImage")
        image_loc = self.get_argument("image", None)
        if image_loc:
            print(image_loc)
            img  = open(image_loc, "r")
            self.set_header ('Content-Type', 'image/jpg')
            #self.set_header ('Content-Disposition', 'attachment; filename='+filename+'')
            #self.write (image_loc)
            self.write (img.read())


        else:
            return self.write("No img")


class LoginHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")

        # with open('/root/users.json') as data_file:
        #     users = json.load(data_file)

        users = list(self.mdb.users.find({"user": username}))

        print(username)
        print(users)

        if len(users) == 1:
            print("tento uzivatel existuje")
            user = users[0]
            if user['pass'] == hashlib.md5(password.encode()).hexdigest():
                self.set_current_user(username)
                self.redirect(self.get_argument("next", u"/"))
            else:
                self.clear_cookie("user")
                self.redirect("/")
        else:
            self.clear_cookie("user")
            self.redirect("/")

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", str(user))
        else:
            self.clear_cookie("user")



class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect(u"/")



class NodeHandler(BaseHandler):
    def get(self, node):
        print(self.current_user)
        user_data = self.get_current_user()

        if self.current_user:
            try:
                params = rosparam.get_param("/arom/node/"+node)
                self.render("../template/node.hbs", user_data=user_data, NavItems=[], NodeParams = params, FeatureParams = None)
            except Exception as e:
                self.render("../template/nonode.hbs", user_data=user_data, NavItems=[], NodeParams = None, FeatureParams = None)
        else:
                self.render("../template/loggedout.hbs")



class MainHandler(BaseHandler):
    def get(self):
        user_data = self.get_current_user()
        self.render("../template/home.hbs", user_data=user_data, NavItems=[])


class WebApi(BaseHandler):
    def get(self, node):
        self.write("Hi")

class WebUpload(BaseHandler):
    def put(self, node):
        data = json.loads(self.request.body)
        print(json.dumps(data, indent=4, sort_keys=False))
        print("test", '/'+node)

        with io.open('/'+node, 'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False)))
