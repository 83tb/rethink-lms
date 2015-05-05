#!/usr/bin/env python

import  logging
from tornado.ioloop import IOLoop
import tornado.web
import os.path
import rethinkdb as r
from tornado import httpserver
from time import time
from tornado import gen
from tornado.options import define, options, parse_command_line
import json
from tornado.escape import json_decode

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

def setup_db(db_name="engine", tables=['lamps',]):
    connection = r.connect(host="localhost")
    try:
        r.db_create(db_name).run(connection)
        for tbl in tables:
            r.db(db_name).table_create(tbl, durability="hard").run(connection)
        logging.info('Database setup completed.')
        # r.db(db_name).table('lamps').index_create('location', geo=True).run(connection)

    except r.RqlRuntimeError:
        logging.warn('Database/Table already exists.')
    finally:
        connection.close()


class EngineApp(tornado.web.Application):

    def __init__(self, db):



        handlers = [
            (r"/", MainHandler),
            (r"/lamps", LampsHandler),
            (r"/feed/lamps", LampFeedHandler),
        ]

        settings = dict(cookie_secret="_asdfasdaasdfasfas",
                        template_path=os.path.join(
                            os.path.dirname(__file__), "templates"),
                        static_path=os.path.join(
                            os.path.dirname(__file__), "static"),
                        xsrf_cookies=False,
                        debug=options.debug)
        self.db = db
        logging.info(db)
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.db = self.application.db
        self.lamps = r.table("lamps")


class MainHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        return self.render('index.html')


class LampsHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        curs = yield self.lamps.run(self.db)
        lamps = []
        while (yield curs.fetch_next()):
            item = yield curs.next()
            # item['location'] = item['location'].to_geojson()

            lamps.append(item)

        self.write(dict(response=lamps))


    @gen.coroutine
    def post(self):
        resource_doc = self.request.body
        print resource_doc
        lamp = json.loads(resource_doc.replace("'", "\""))
        lamps = (yield self.lamps.insert(lamp).run(self.db))
        # print lamps
        lamp['id'] = lamps['generated_keys'][0]
        self.write(lamp)
        
    @gen.coroutine
    def patch(self):
        resource_doc = self.request.body
        lamp = json.loads(resource_doc.replace("'", "\""))
        lamps = (yield self.lamps.update(lamp).run(self.db))
        self.write(lamp)

class LampFeedHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        curs = yield self.lamps.changes().run(self.db)

        while (yield curs.fetch_next()):
            feed = yield curs.next()
            lamp = {
                'id': feed['new_val']['id'],
                'html': tornado.escape.to_basestring(
                    self.render_string("lamp.html",
                                       lamp=feed['new_val']))}
            break

        self.finish(dict(lamps=[lamp]))


@gen.coroutine
def main():
    """ Async main method. It needed to be async due to r.connect is async . """
    parse_command_line()
    db_name = "engine"
    setup_db(db_name)
    r.set_loop_type("tornado")
    db = yield r.connect("localhost", db=db_name)
    http_server = httpserver.HTTPServer(EngineApp(db))
    http_server.listen(options.port)


if __name__ == "__main__":
    IOLoop.current().run_sync(main)
    IOLoop.current().start()
