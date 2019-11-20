import argparse
import json
import base64

import tornado.ioloop
import tornado.web

parser = argparse.ArgumentParser(description='set server commandline argument')

parser.add_argument(
    '-p',
    '--port',
    type=int,
    default=8888,
    required=False,
    help='set listening port'
    )

args = parser.parse_args()


class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        with open('../files/lena_gray_256.tif', 'rb') as f:
            self.org_data = f.read()

    def get(self):
        self.write('Hello, world')

    def post(self):
        data = json.loads(self.request.body)
        k, v = data.popitem()
        raw_data = base64.b64decode(v)

        # check data
        if self.org_data == raw_data:
            self.write(json.dumps({'code': 0, 'message': 'check ok'}))
        else:
            self.write(json.dumps({'code': 1, 'message': 'check failed'}))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(args.port)
    print(f'start server, listen port: {args.port}')
    tornado.ioloop.IOLoop.current().start()

