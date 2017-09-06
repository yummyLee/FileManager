import json
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import get_disk_info

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
                files = os.listdir(path + "\\")
                files_info = []
                for file in files:
                    if os.path.isdir(path + "\\" + file):
                        files_info.append({"fileName": file, "fileType": "dir"})
                    else:
                        files_info.append({"fileName": file, "fileType": "file"})
                self.write(json.dumps(files_info))
            if param == "find":
                path = self.get_argument("path")
                print("---" + path)
                path_segment = path.split('\\')
                disk_info = get_disk_info.get_fs_info()
                dir_info = []
                for i in disk_info:
                    dir_info.append({"file_name": i["Caption"], "file_type": "dir",
                                     "file_path": i["Caption"] + "\\"})
                result = []
                print(dir_info)
                for i in range(len(path_segment)):
                    print(path_segment[i])
                    for j in dir_info:
                        if path_segment[i] == j["file_name"] or path_segment[i] == "":
                            path_segment[i] = "found"
                            if os.path.isdir(j["file_path"]):
                                dir_files = os.listdir(j["file_path"])
                                dir_info.clear()
                                for f in dir_files:
                                    is_dir = os.path.isdir(j["file_path"] + f)
                                    if is_dir:
                                        is_dir = "dir"
                                    else:
                                        is_dir = "file"
                                    dir_info.append({"file_name": f, "file_type": is_dir,
                                                     "file_path": j["file_path"] + f + "\\"})
                                result.append(
                                    {"file_name": j["file_name"], "file_path": j["file_path"], "dir_files": dir_files})
                            else:
                                result.append(
                                    {"file_name": j["file_name"], "file_path": j["file_path"], "dir_files": "final"})
                if path_segment[len(path_segment) - 1] != "found":
                    result = []
                print(result)
                self.write(json.dumps(result))

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
