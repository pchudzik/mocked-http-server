import argparse

from http.server import BaseHTTPRequestHandler, HTTPServer
from random import random
import json

arg_parser = argparse.ArgumentParser(
    description='Simple http server which will to serve request with specified ratio and errors')
arg_parser.add_argument(
    "--port",
    help="Port on which server will listen",
    default=8181,
    type=int)
arg_parser.add_argument(
    "--error-ratio",
    help="Error ratio. 0.2 means 20% of requests will fail",
    type=float)
arg_parser.add_argument(
    "--error-file",
    help="File with errors to be send to user (one by one)",
    required=False)
arg_parser.add_argument(
    "--success-file",
    help="File with success responses to be send to user (one by one)",
    required=False)
arg_parser.add_argument(
    "--path",
    help="Path under which all requests will be served",
    default="/api")


def load_responses(location):
    if location:
        with open(location) as file:
            return infinite_generator(json.load(file))


def infinite_generator(collection):
    while True:
        for item in collection:
            yield item


def create_handler_factory(config):
    available_errors = load_responses(config.error_file)
    available_success = load_responses(config.success_file)

    def handler_factory(request, client_address, server):
        return FailingHandler(
            request, client_address, server,
            next(available_errors) if random() < config.error_ratio else next(available_success))

    return handler_factory


class FailingHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, server_response):
        self.server_response = server_response
        super().__init__(request, client_address, server)

    def do_GET(self):
        if self.path != config.path:
            return self.__send_response({"status": 404, "response_json": {"error": "Not Found"}})
        return self.__send_response(self.server_response)

    def __send_response(self, response):
        self.send_response(response["status"])
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response["response_json"]).encode())


if __name__ == "__main__":
    config = arg_parser.parse_args()
    try:
        server = HTTPServer(('', config.port), create_handler_factory(config))
        print(f"Started httpserver on port {config.port}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("shutting down the server")
        server.socket.close()
