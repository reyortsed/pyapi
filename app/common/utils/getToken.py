import base64
import hashlib
import os
import urllib.parse
import webbrowser
import requests

# The Azure Tenant which will serve as identity provider
TENANT_ID = "f57aa600-9672-40c1-a836-3981a7d7d95f" 

# Register a client app for token requests
CLIENT_ID = "2e415397-7154-48b9-b2ed-22f5e2f59805"  

# Register an app for the API itself with appropriate scope (See under)
API_CLIENT_ID = "705a8871-0d6c-4a08-85bd-9242381ab523"  

# Callback URL for token request. 
# This must match exacly with one of the client app callback urls
# registered on identity provider.
# Controller is also in api atm, for simplicty
REDIRECT_URI = "https://localhost/callback" 

# Scope determines what permissions the client app will have to info from identity provider.
SCOPE = f"api://pythonapi_v2/access_as_user openid offline_access" 


# Workaround. Azure wouldnt give me a jwt without passing back an opaque token first
# Must generate PKCE verifier & challenge to retrieve an opaque token
def generate_pkce():
    verifier = base64.urlsafe_b64encode(os.urandom(40)).rstrip(b"=").decode("utf-8")
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode("utf-8")).digest()
    ).rstrip(b"=").decode("utf-8")
    return verifier, challenge

verifier, challenge = generate_pkce()

# The Auth Url we send our opaque token request to
auth_url = (
    f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize?"
    + urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "response_mode": "query",
        "scope": SCOPE,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": "12345"
    })
)

print("\nOpen the following URL in your browser and log in:")
print(auth_url)
webbrowser.open(auth_url)

# We get back an opaque token that then needs to be resent
code = input("\nPaste the opaque token from the redirect URL: ").strip()

# Request the jwt
token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
data = {
    "client_id": CLIENT_ID,
    "scope": SCOPE,
    "code": code,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code",
    "code_verifier": verifier,
}

resp = requests.post(token_url, data=data)
resp.raise_for_status()

tokens = resp.json()
print(tokens["access_token"]) # This can now be used to authorize client