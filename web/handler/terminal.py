#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.escape
import tornado.web

import glob
import json
import io
import subprocess
import time, datetime
import os, sys
import glob
import random

import pymongo
from bson.json_util import dumps
import bson





class TerminalHandler(tornado.web.RequestHandler):
	pass
    # def get_current_user(self):

    #     user_file = '/root/users.json'

    #     #if not os.path.exists(user_file):
    #     #    print "Missing user.json (%s)" %(user_file)
    #     #    sys.exit()

    #     user_json = self.get_secure_cookie("user")
    #     with open(user_file) as data_file:
    #         users = json.load(data_file)

    #     if user_json:
    #         return users[eval(user_json)]
    #     else:
    #         return None

    # def initialize(self):
    #     #self.config = self.settings['']
    #     #self.db = self.settings['']
    #     pass

    # def get_login_url(self):
    #     return u"/login"


class home(TerminalHandler):
	def get(self):
		self.render('terminal/term.home.hbs')

class run_program(TerminalHandler):
	def get(self, queue_id):
		print("run_program()", queue_id)

		mdb = pymongo.MongoClient("mongodb://localhost:27017/").IRRADROOM
		program = list(mdb.runs.find({'run_key': int(queue_id) }))

		if len(program) > 0:
			program = program[0]

		self.write(dumps(program))