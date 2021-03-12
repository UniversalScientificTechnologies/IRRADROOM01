
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado
#import rosnode

class WeatherInfo(tornado.web.UIModule):

    def render(self):
        return self.render_string("modules/WeatherInfo.hbs")
        #return "self.render_string()"


class NavBar(tornado.web.UIModule):
    def render(self):
        #rosnode.rosnode_listnodes(list_all=True)
        return self.render_string("nav.hbs", navItems = [])


class NodeFeature(tornado.web.UIModule):
    def render(self, node, *args, **kwds):
        #return globals()[node](self, *args, **kwds).value()
        print(args)
        try:
            print("node name>>", node.split("__")[0])
            if 'external' == node.split("__")[0]:
                return self.render_string(args[0]['feature'], FeatureParams = args[0])
            else:
                return self.render_string("modules/features/%s.hbs"%(node.split("__")[0]), FeatureParams = args[0])
                pass
        except Exception as e:
            print(e)
            return self.write( e )
