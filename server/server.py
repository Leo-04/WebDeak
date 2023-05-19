from server.web_server import WebServer
from http.server import HTTPServer
import socket
from threading import Thread

MY_IP = socket.gethostbyname(socket.gethostname())


class ServerThread:
    def __init__(self):
        self.active = False
        self.thread = None
        self.server = None
        self.web_server = None

    def start(self, layout, page_html, index_html, error_html, access_denied_html, whitelist, host=MY_IP, port=8080):
        """Starts a server if one is not running"""

        if self.thread is None:
            self.active = True
            self.thread = Thread(target=self.run,
                                 args=(layout, page_html, index_html, error_html, access_denied_html, whitelist, host,
                                       port))
            self.thread.start()

    def stop(self):
        """Stops current server"""

        self.active = False

    def run(self, layout, page_html, index_html, error_html, access_denied_html, whitelist, host=MY_IP, port=8080):
        """Thread loop"""

        whitelist.append(host)
        self.web_server = WebServer(layout, page_html, index_html, error_html, access_denied_html, whitelist)
        self.server = HTTPServer((host, port), self.web_server.HTTPRequestHandler)
        self.server.timeout = 1

        print("http://" + (str(host) if host else "localhost") + ":" + str(port))

        self.active = True

        while self.active:
            self.server.handle_request()

        self.server.server_close()

        self.thread = None
