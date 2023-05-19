import io
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import unquote, quote
import base64
import math
import os


class WebServer:
    def __init__(self, layout, page_html, index_html, error_html, access_denied_html, whitelist):
        self.layout = layout
        self.html = page_html
        self.index = index_html
        self.error = error_html
        self.access_denied = access_denied_html
        self.whitelist = whitelist

    def HTTPRequestHandler(self, socket, address, server):

        class Hwnd(BaseHTTPRequestHandler):
            timeout = 1

            do_GET = lambda hwnd: self.http_get(hwnd)
            do_POST = lambda hwnd: self.http_post(hwnd)

        return Hwnd(socket, address, server)

    def http_get(self, hwnd):
        ip = hwnd.client_address[0]
        name = unquote(hwnd.path)[1:]

        hwnd.send_response(200)
        hwnd.send_header("Content-type", "text/html")
        hwnd.end_headers()

        items = ""
        width = 100
        height = 100

        if ip not in self.whitelist:
            html = self.access_denied

        elif name == "":
            html = self.index

            for name in self.layout:
                if name:
                    items += f"<button class='text' onclick='window.location = \"./{quote(name)}\"'> {name} </button>"

        elif name in self.layout:
            num_cols, buttons = self.layout[name]
            html = self.html

            i = 0
            while i < len(buttons):
                items += "<tr>"
                for x in range(num_cols):
                    if i >= len(buttons):
                        break

                    items += f"<td onclick='send({i})'>"
                    if buttons[i][3]:
                        try:
                            with open(buttons[i][3], "rb") as fp:
                                data = base64.b64encode(fp.read())
                            data_string = data.decode("utf-8")

                            items += f"<button class='image text'"
                            items += f"style='background-image: url(data:image/png;base64,{data_string}); "
                        except Exception as err:
                            print(f"Cannot open file {buttons[i][3]}\nReason: "+str(err))
                            items += f"<button class='text' style='"
                    else:
                        items += f"<button class='text' style='"

                    items += f"{buttons[i][2]}'>{buttons[i][0]}"
                    items += f"</button>"
                    items += "</td>"
                    i += 1
                items += "</tr>"

            width = 100 // num_cols
            height = 100 // math.ceil(len(buttons) / num_cols)
        else:
            html = self.error

        page = (
            html.replace("{{ITEMS}}", items)
            .replace("{{WIDTH}}", str(width))
            .replace("{{HEIGHT}}", str(height))
            .replace("{{GLOBAL CSS}}", self.layout[""])
            .replace("{{IP}}", ip)
        )

        hwnd.wfile.write(page.encode("UTF-8"))
        hwnd.wfile.flush()

        return

    def http_post(self, hwnd):
        ip = hwnd.client_address[0]
        name = unquote(hwnd.path)[1:]

        data = {}

        if ip not in self.whitelist:
            data["access denied"] = "access denied"

        elif name == "":
            data["msg"] = "hello world"

        elif name in self.layout:

            content_length = int(hwnd.headers['Content-Length'])

            number_str = hwnd.rfile.read(content_length)
            try:
                cmd = self.layout[name][1][int(number_str)][1]

                print(cmd)

                value = os.popen(cmd)
                data["read"] = value.read()
            except Exception as err:
                print(err)

                data["error"] = str(err)
        else:
            data["error"] = name

        hwnd.send_response(200)
        hwnd.send_header('Content-type', 'text/json')
        hwnd.end_headers()
        hwnd.wfile.write(json.dumps(data).encode("UTF-8"))
        hwnd.wfile.flush()

        return
