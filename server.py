from flask import Flask, redirect, request, jsonify, render_template_string, send_file
import json
import os

app = Flask(__name__)

# The URL Garena redirects to after login — change to your domain + /cookie-capture
REDIRECT_URI = "https://cookiegeb-1.onrender.com/cookie-capture"

# Garena login URL with redirect to your cookie capture page
GARENA_LOGIN_URL = (
    "https://sso.garena.com/universal/login?"
    "app_id=10100&"
    f"redirect_uri={REDIRECT_URI}&"
    "locale=en-PH"
)

COOKIE_FILE = "user_cookies.json"


@app.route("/")
def home():
    return (
        "Welcome! Use /login to login to Garena and generate your cookies.<br>"
        "Then visit /getcookie to download your cookie file."
    )


@app.route("/login")
def login():
    # Redirect user to Garena login page
    return redirect(GARENA_LOGIN_URL)


@app.route("/cookie-capture", methods=["GET"])
def cookie_capture():
    # Serve a simple HTML + JS page that grabs accessible cookies and sends them to server
    page = """
    <!DOCTYPE html>
    <html>
    <head><title>Cookie Capture</title></head>
    <body>
      <h2>Cookie Capture Page</h2>
      <p>If you are seeing this, login was successful and we are capturing your cookies now...</p>
      <script>
        function sendCookies() {
          const cookies = document.cookie;
          fetch("/save_cookies", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cookies: cookies })
          }).then(res => {
            if(res.ok){
              document.body.innerHTML += "<p>Cookies saved! You can now close this page and return to your bot.</p>";
            } else {
              document.body.innerHTML += "<p>Failed to save cookies.</p>";
            }
          }).catch(() => {
            document.body.innerHTML += "<p>Error sending cookies.</p>";
          });
        }
        sendCookies();
      </script>
    </body>
    </html>
    """
    return render_template_string(page)


@app.route("/save_cookies", methods=["POST"])
def save_cookies():
    data = request.get_json()
    cookies_str = data.get("cookies", "")
    if not cookies_str:
        return jsonify({"error": "No cookies sent"}), 400
    
    # Save cookies string in JSON file
    with open(COOKIE_FILE, "w") as f:
        json.dump({"cookies": cookies_str}, f)
    
    return jsonify({"status": "Cookies saved"}), 200


@app.route("/getcookie", methods=["GET"])
def get_cookie_file():
    # Return the saved cookie file to user
    if not os.path.exists(COOKIE_FILE):
        return "No cookie file found. Please login first.", 404
    return send_file(COOKIE_FILE, mimetype="application/json", as_attachment=True, download_name="cookie.json")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
