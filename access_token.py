import argparse

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

oauth = (
    "https://accounts.google.com/o/oauth2/v2/auth?"
    "scope={scope}"
    "&response_type=code"
    "&client_id={client_id}"
    "&redirect_uri=urn:ietf:wg:oauth:2.0:oob"
).format(scope=args.scope, client_id=args.client_id)

print("Open this URL in your browser and follow the steps:\n\n{}\n".format(oauth))

authorization_code = input("Paste the code here: ")

tokens = requests.post("https://www.googleapis.com/oauth2/v4/token",
                       params={
                           'code': authorization_code,
                           'client_id': args.client_id,
                           'client_secret': args.client_secret,
                           'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
                           'grant_type': 'authorization_code'
                       },
                       headers={
                           'Content-Type': 'application/x-www-form-urlencoded'
                       }
                       ).json()

print()
print(tokens)
