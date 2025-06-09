from flask import Flask, redirect, request, jsonify, send_file
import os

app = Flask(__name__)

# Your URL to redirect users after login (Garena account dashboard)
REDIRECT_AFTER_LOGIN = "https://account.garena.com/"

@app.route("/login")
def login_redirect():
    # Garena official SSO login URL with redirect back to your site if needed
    garena_login_url = (
        "https://sso.garena.com/universal/login?"
        "app_id=10100&"
        f"redirect_uri={REDIRECT_AFTER_LOGIN}&"
        "locale=en-PH"
    )
    return redirect(garena_login_url)

# ... rest of your code (save_cookies, get_cookie_file) ...
