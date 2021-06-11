
import os
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.web
import tornado.speedups

import rclpy
from rclpy.node import Node

tornado.options.define("port", default=8080, help="port", type=int)
tornado.options.define("debug", default=True, help="debug mode")

from handler import base, terminal
from modules import modules

class WebApp(tornado.web.Application):

    def __init__(self, config={}):

        handlers = [
            (r"/", base.MainHandler),
            #(r"/node/pymlab_node", pymlab_handler.pymlabBase),
            #(r"/node/(.*)", base.NodeHandler),
            #(r"/rosapi/publist/(.*)", rosHandlers.publish),
            (r"/login", base.LoginHandler),
            (r"/logout", base.LogoutHandler),
            #(r"/api/upload/(.*)", base.WebUpload),
            #(r"/api/getImage/(.*)", base.GetImage),
            #(r"/api/node/kill/(.*)", base.NodeKill),
            #(r"/api/node/start/(.*)", base.NodeStart),
            (r"/state", base.State),
            (r"/controller", base.Controller),
            (r"/controller/get_programs", base.Controller_get_programs),
            (r"/controller/get_program/(.*)", base.Controller_get_program),
            (r"/controller/queue_program/(.*)", base.Controller_queue_program),
            (r"/controller/edit_program/(.*)/(.*)/", base.Controller_edit_program),
            (r"/controller/update_program/(.*)/", base.Controller_update_program),
            (r"/controller/remove_program_step/(.*)/(.*)/", base.Controller_remove_program_step),
            (r"/controller/create_program", base.Controller_create_program),
            (r"/poweroff", base.PowerOff),

            (r"/controller/get_jobs", base.Controller_get_jobs),

            (r"/terminal/run_program_from_terminal/(.*)/", terminal.run_program),
            (r"/terminal/", terminal.home),
            #(r"/rosapi/(.*)", rosHandlers.NodeHandler),
            #(r"/ws/(.*)", websockets.PanWebSocket),
        ]


        settings = dict(
            cookie_secret="necovelmimocanejvictajnyretezeckterynikdoneu",
            #template_path=os.path.join(self._base_dir, "template"),
            template_path= "/root/dev_ws/IRRADROOM01/web/template",
            #static_path=os.path.join(self._base_dir, "static"),
            static_path= "/root/dev_ws/IRRADROOM01/web/static/",
            #xsrf_cookies=True,
            xsrf_cookies=False,
            name="UST.cz",
            #server_url=server_url,
            site_title= "UST.cz",
            ui_modules= modules,
            port=tornado.options.options.port,
            compress_response=True,
            debug=tornado.options.options.debug,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(WebApp())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()
