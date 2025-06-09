from flask import Flask, request, redirect, make_response, jsonify, render_template_string

app = Flask(__name__)
SESSIONS = {}

@app.route("/login", methods=["GET", "POST"])
def login():
    token = request.args.get("token")
    user_id = request.args.get("user_id")
    if request.method == "POST":
        session_cookie = f"session-{user_id}"
        SESSIONS[token] = session_cookie
        resp = make_response(redirect("/set_cookie"))
        resp.set_cookie("sessionid", session_cookie)
        return resp
    return """
    <form method='post'>
      <input name='username'><br>
      <input name='password' type='password'><br>
      <input type='submit'>
    </form>
    """

@app.route("/set_cookie")
def set_cookie():
    return "Login complete. Return to Telegram."

@app.route("/get_cookie/<token>")
def get_cookie(token):
    cookie = SESSIONS.get(token)
    if cookie:
        return jsonify({"cookie": cookie})
    return jsonify({}), 404
