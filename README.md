# Access Token

A Python script to manually obtain an OAuth 2.0 access token and a refresh token for Google APIs using a Client ID, a Client secret and an access scope. The exchange is based on the authorization code grant.

## Usage

```sh
access-token --client-id     CLIENT_ID     \
             --client-secret CLIENT_SECRET \
             --scope         SCOPE
```
If arguments are not supplied they will be promted for:
```sh
access-token
```
