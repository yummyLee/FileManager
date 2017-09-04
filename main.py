import os.path
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import get_disk_info
import json

from tornado.options import define, options

define("port", default=8007, help="help", type=int)


class MainHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):

        param = self.get_argument("param", None)
        if param is not None:
            if param == "disk_info":
                self.write(json.dumps(get_disk_info.get_fs_info()))
            if param == "dir_info":
                path = self.get_argument("path")
                print("---" + path)
                files = os.listdir(path+"\\")
                files_info = []
                for file in files:
                    if os.path.isdir(path + "\\" + file):
                        files_info.append({"fileName": file, "fileType": "dir"})
                    else:
                        files_info.append({"fileName": file, "fileType": "file"})
                self.write(json.dumps(files_info))
        else:
            self.render("index.html")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/index.html", MainHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            autoescape=None
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
