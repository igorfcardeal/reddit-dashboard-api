from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
import requests, os

app = FastAPI()

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDDIT_REDIRECT_URI")

@app.get("/")
def root():
    return {"status": "ok", "message": "API funcionando 🚀"}

@app.get("/oauth/start")
def oauth_start():
    url = (
        f"https://www.reddit.com/api/v1/authorize?"
        f"client_id={CLIENT_ID}&response_type=code&state=xyz&redirect_uri={REDIRECT_URI}"
        f"&duration=permanent&scope=read,modlog,modmail"
    )
    return RedirectResponse(url)

@app.get("/oauth/callback")
def oauth_callback(code: str):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    auth = (CLIENT_ID, CLIENT_SECRET)
    headers = {"User-Agent": "empresa-dashboard/1.0"}
    r = requests.post("https://www.reddit.com/api/v1/access_token", data=data, auth=auth, headers=headers)
    return r.json()

@app.get("/metrics/{subreddit}")
def get_metrics(subreddit: str):
    headers = {
        "Authorization": f"bearer {os.getenv('REDDIT_ACCESS_TOKEN')}",
        "User-Agent": "empresa-dashboard/1.0",
    }
    r = requests.get(f"https://oauth.reddit.com/r/{subreddit}/about/traffic", headers=headers)
    if r.status_code != 200:
        return JSONResponse({"error": "não consegui pegar os dados"}, status_code=400)
    return r.json()
