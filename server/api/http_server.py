"""
This server will receive post requests containing an object that need to be detected on screen.
This server will be used in a special mode of the program.
"""
"""
This server will receive HTTP post requests and send the data to flask
"""
from threading import Thread
import http.server
import json
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer

class S(BaseHTTPRequestHandler):

    def __init__(self,shared_variables, *args, **kwargs):
        self.CRYPT = "password-1"
        self.shared_variables = shared_variables
        super().__init__(*args, **kwargs)

    def _set_response(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS, HEAD, GET')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_response()

    def do_OPTIONS(self):
        self._set_response()

    def clear_timer():
        self.shared_variables.SHOW_ONLY = []

    def do_POST(self):
        #print(self.client_address,self.headers)

        if self.headers['Content-Length']:

            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            # decode incoming data // see if password is correct here!
            try:
                data = json.loads(post_data)
                print(data)
                """
                Data struct:
                    data = {
                'value': "person",
                'type': 'add',
                'api_crypt':"password-1"
                    }
                """
                if data['api_crypt'] :
                    if data['api_crypt'] == self.CRYPT:
                        if data["value"]:
                            if data["type"] == "remove":
                                print("Removed Class : "+ str(data["value"]))
                                for box in self.shared_variables.list:
                                    if box.classification == data["value"]:
                                        box.remove() # stop running boxes!
                                if data["value"] in self.shared_variables.SHOW_ONLY:
                                    self.shared_variables.SHOW_ONLY.remove(data["value"])
                            else:
                                if not data["value"] in self.shared_variables.SHOW_ONLY:
                                    print("Added Class : "+ str(data["value"]))
                                    self.shared_variables.SHOW_ONLY.append(data["value"])
            except Exception as e:
                print("ERROR: "+str(e))
        self._set_response()

class HTTPserver(Thread):

    def __init__(self, shared_variables):
        super().__init__()
        self.shared_variables = shared_variables
    def run(self):
        server_address = ("127.0.0.1",5000)
        httpd = HTTPServer(server_address, partial(S, self.shared_variables))
        try:
            print("HTTP Server Started!")
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()

def safe(json, value):
    try:
        return json[value]
    except Exception:
        return
