#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import simplejson

from collector import collect

class SystemValuesRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

        values = collect()
        serialized_vals = bytes(simplejson.dumps(values), 'utf8')
        self.wfile.write(serialized_vals)
        return

def run():
    server_addr = ('127.0.0.1', 6649)
    httpd = HTTPServer(server_addr, SystemValuesRequestHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
