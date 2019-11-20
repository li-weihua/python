import argparse
import json
import hashlib

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
    def post(self):
        files = self.request.files

        iter_file = iter(files)
        first = next(iter_file)

        if first != 'json':
            return
        bstring = files[first][0]['body']
        json_data = json.loads(bstring.decode('utf-8'))
        print(json_data)

        file_hash = json_data['file_hash']

        status = True
        for k in iter_file:
                if hashlib.md5(files[k][0]['body']).hexdigest() == file_hash[k]:
                    print(f'{k}: check ok!')
                else:
                    status = False
                    print(f'{k}: check failed')

        if status:
            self.write(json.dumps({'code': 0, 'message': 'file check ok'}))
        else:
            self.write(json.dumps({'code': 1, 'message': 'file check failed'}))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(args.port)
    print(f'start server, listen port: {args.port}')
    tornado.ioloop.IOLoop.current().start()

