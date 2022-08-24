import argparse
import http.server
import json
from urllib import parse

import requests


parser = argparse.ArgumentParser(description='Generate access and refresh tokens for Google APIs.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--client-id', type=str, help='the Client ID of the app')
parser.add_argument('--client-secret', type=str, help='the Client secret of the app')
parser.add_argument('--scope', type=str, help='the scope of the request')
args = parser.parse_args()

if args.client_id is None:
    args.client_id = input("Paste the Client ID: ")
if args.client_secret is None:
    args.client_secret = input("Paste the Client secret: ")
if args.scope is None:
    args.scope = input("Paste the scope: ")

print()

# Construct the URL

oauth = "https://accounts.google.com/o/oauth2/v2/auth?" \
    f"scope={args.scope}" \
    "&access_type=offline" \
    "&response_type=code" \
    f"&client_id={args.client_id}" \
    "&redirect_uri=http://localhost"

print(f"Open this URL in your browser and follow the steps:\n\n{oauth}\n")

# Receive authorization code

class Handler(http.server.BaseHTTPRequestHandler):
    authorization_code = None
    def do_GET(self):
        parameters = parse.parse_qs(parse.urlparse(self.path).query)
        if 'code' in parameters:
            self.send_response(200, "OK")
            self.end_headers()
            Handler.authorization_code = parameters['code']
            self.wfile.write("You can close this tab now and switch to the terminal.".encode("utf-8"))
        else:
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write("Didn't receive authorization code.".encode("utf-8"))
with http.server.HTTPServer(("localhost", 80), Handler) as httpd:
    while not Handler.authorization_code:
        httpd.handle_request()

authorization_code = Handler.authorization_code

print()

# Retrieve access and refresh tokens

tokens = requests.post("https://www.googleapis.com/oauth2/v4/token",
                       params={
                           'code': authorization_code,
                           'client_id': args.client_id,
                           'client_secret': args.client_secret,
                           'redirect_uri': 'http://localhost',
                           'grant_type': 'authorization_code'
                       },
                       headers={
                           'Content-Type': 'application/x-www-form-urlencoded'
                       }
                       ).json()

print(json.dumps(tokens, indent=4))
