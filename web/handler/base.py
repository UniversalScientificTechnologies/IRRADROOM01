#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.escape
import tornado.web

import glob
import json
import io
import os, sys
import subprocess
import sqlite3


#import rosparam
import hashlib

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):

        user_file = '/root/users.json'

        #if not os.path.exists(user_file):
        #    print "Missing user.json (%s)" %(user_file)
        #    sys.exit()

        user_json = self.get_secure_cookie("user")
        with open(user_file) as data_file:
            users = json.load(data_file)

        if user_json:
            return users[eval(user_json)]
        else:
            return None

    def initialize(self):
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
        con = sqlite3.connect('~/irradroom.db')

class Controller_create_program(BaseHandler):
    def get(self):
        con = sqlite3.connect('/root/irradroom.db')
        cur = con.cursor()
        cur.execute("INSERT INTO programs ('created', 'name', 'author_system', 'author_name') VALUES (datetime('now'), 'Nový program', 'Autor', 'Autor')")
        print(cur.lastrowid)
        con.commit()

        data = {"program_id": cur.lastrowid}
        self.write(data)


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

        with open('/root/users.json') as data_file:
            users = json.load(data_file)

        print(username)
        print(users)

        if username in users:
            print("tento uzivatel existuje")
            print(users[username])
            if users[username]['pass'] == hashlib.md5(password.encode()).hexdigest():
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
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
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
