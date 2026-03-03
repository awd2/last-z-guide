import json
import urllib.parse
import urllib.request
import webbrowser

CLIENT_ID = input('Client ID: ').strip()
CLIENT_SECRET = input('Client Secret: ').strip()

REDIRECT_URI = "http://localhost:8080"
SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"

params = {
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "response_type": "code",
    "scope": SCOPE,
    "access_type": "offline",
    "prompt": "consent",
}

url = AUTH_URL + "?" + urllib.parse.urlencode(params)
print("Open this URL in browser:")
print(url)
try:
    webbrowser.open(url)
except Exception:
    pass

code = input("Paste code from URL here: ").strip()

data = urllib.parse.urlencode(
    {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
).encode("utf-8")

req = urllib.request.Request(
    TOKEN_URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}
)
with urllib.request.urlopen(req, timeout=30) as resp:
    payload = json.loads(resp.read().decode("utf-8"))

print("\nTokens:")
print(json.dumps(payload, indent=2))

if "refresh_token" in payload:
    print("\nRefresh token:")
    print(payload["refresh_token"])
else:
    print("\nNo refresh_token returned. Try again with prompt=consent and ensure it's the first consent for this client.")
