from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

# In-memory store to link Telegram user IDs and their cookie files (for demo)
user_cookie_files = {}

@app.route("/login")
def login_page():
    return """
    <h2>Login to Garena</h2>
    <p>Please login, and then send your Telegram user ID to the bot.</p>
    """

@app.route("/save_cookies", methods=["POST"])
def save_cookies():
    data = request.json
    telegram_user_id = data.get("user_id")
    cookies = data.get("cookies")

    if not telegram_user_id or not cookies:
        return jsonify({"error": "Missing user_id or cookies"}), 400

    # Save the cookies to a python file for this user
    filename = f"cookies_{telegram_user_id}.py"
    with open(filename, "w") as f:
        f.write("def get_cookies():\n")
        f.write("    return {\n")
        for name, value in cookies.items():
            f.write(f'        "{name}": "{value}",\n')
        f.write("    }\n")

    user_cookie_files[telegram_user_id] = filename
    return jsonify({"status": "success", "filename": filename})

@app.route("/get_cookie_file/<user_id>")
def get_cookie_file(user_id):
    filename = f"cookies_{user_id}.py"
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    else:
        return "Cookie file not found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
