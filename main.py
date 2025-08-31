import mimetypes
import pathlib
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

from message_processor import MessageProcessor, MessageFactory
from renderer import Renderer


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }
        message = MessageFactory.create(**data_dict)
        MessageProcessor.append_message(message)
        self.send_response(302)
        self.send_header("Location", "/read")
        self.end_headers()

    def do_GET(self):
        try:
            pr_url = urllib.parse.urlparse(self.path)
            if pr_url.path == "/":
                self.send_html_file("index.html")
            elif pr_url.path == "/message":
                self.send_html_file("message.html")
            elif pr_url.path == "/read":
                self.send_html_file(
                    "read.html", data={"messages": MessageProcessor.load_messages()}
                )
            else:
                if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                    self.send_static()
                else:
                    self.send_html_file("error.html", 404)
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                f"<html><body><h1>Error!</h1><p>{e}</p></body></html>".encode()
            )
            raise e

    def send_html_file(self, filename, status=200, data=None):
        if data is None:
            data = []
        renderer = Renderer()
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(renderer.render(filename, data).encode("utf-8"))

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == "__main__":
    run()
