#!/usr/bin/env python

import logging
from tornado.ioloop import IOLoop
import tornado.web
import os.path
import rethinkdb as r
from tornado import httpserver
from tornado import gen
from tornado.options import define, options, parse_command_line
import json
from tornado.escape import json_decode

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


logger = logging.getLogger('engine')
logger.setLevel(logging.DEBUG)

hdlr = logging.FileHandler('logs/engine.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)


def setup_db(db_name="engine", tables=['lamps', 'settings', 'commands', 'sensors', 'sensor_reads']):
    connection = r.connect(host="localhost")
    try:
        r.db_create(db_name).run(connection)
    except r.RqlRuntimeError:
        logger.warn('Database already exists.')

    for tbl in tables:
        try:
            r.db(db_name).table_create(tbl, durability="hard").run(connection)
        except r.RqlRuntimeError:
            logger.warn('Table already exists.')
    logger.info('Database setup completed.')
    try:
        r.db(db_name).table('lamps').index_create(
            'location', geo=True).run(connection)
    except r.RqlRuntimeError:
        logger.warn('Index already exists.')
    connection.close()


class EngineApp(tornado.web.Application):

    def __init__(self, db):

        handlers = [
            (r"/", MainHandler),
            (r"/lamps", LampsHandler),
            (r"/geolamps", GeoLampsHandler),
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
        logger.info(db)
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.db = self.application.db
        self.lamps = r.table("lamps")

    '''
    CORS support...
    should work but does not... needs more debuging...
    '''

    def set_default_headers(self):
        #        print "setting headers!!!"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


class MainHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        return self.render('index.html')


class GeoLampsHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        resource_doc = self.request.body

        bbox_json = json.loads(resource_doc.replace("'", "\""))
        bbox = r.polygon(
            bbox_json[0], bbox_json[1], bbox_json[2], bbox_json[3])

        curs = yield self.lamps.get_intersecting(bbox, index='location').run(self.db)
        lamps = []
        while (yield curs.fetch_next()):
            item = yield curs.next()
            # item['location'] = item['location'].to_geojson()

            lamps.append(item)

        self.write(dict(response=lamps))

    @gen.coroutine
    def post(self):
        resource_doc = self.request.body

        bbox_json = json.loads(resource_doc.replace("'", "\""))
        bbox = r.polygon(
            bbox_json[0], bbox_json[1], bbox_json[2], bbox_json[3])

        curs = yield self.lamps.get_intersecting(bbox, index='location').run(self.db)
        lamps = []
        while (yield curs.fetch_next()):
            item = yield curs.next()
            # item['location'] = item['location'].to_geojson()

            lamps.append(item)

        self.write(dict(response=lamps))


class LampsHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        # r.table('parks').get_intersecting(circle1, index='area').run(conn)
        curs = yield self.lamps.run(self.db)
        lamps = []
        while (yield curs.fetch_next()):
            item = yield curs.next()
            # item['location'] = item['location'].to_geojson()

            lamps.append(item)

        self.write(dict(response=lamps))

    @gen.coroutine
    def post(self):
        resource_doc = json.loads(self.request.body)

        if isinstance(resource_doc, list):
            for lamp_json in resource_doc:
                lamp = lamp_json
                lamps = (yield self.lamps.insert(lamp).run(self.db))

        else:
            lamp = json.loads(resource_doc)
            lamps = (yield self.lamps.insert(lamp).run(self.db))

    @gen.coroutine
    def patch(self):
        resource_doc = json.loads(self.request.body)

        if isinstance(resource_doc, list):
            for lamp_json in resource_doc:
                lamp = lamp_json
                lamps = (yield self.lamps.update(lamp).run(self.db))

        else:
            lamp = json.loads(resource_doc)
            lamps = (yield self.lamps.update(lamp).run(self.db))


class LampFeedHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        curs = yield self.lamps.changes().run(self.db)

        while (yield curs.fetch_next()):
            feed = yield curs.next()

        self.finish(dict(lamps=[feed]))


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
