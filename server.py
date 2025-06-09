from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "https://sso.garena.com/universal/login?app_id=10100&redirect_uri=https%3A%2F%2Faccount.garena.com%2F&locale=en-PH!"

@app.route("/generate-cookie")
def generate_cookie():
    # Example cookie data
    cookie = {
        "_ga_1M7M9L6VPX": "GS2.1.s1749383929$o1$g0$t1749384032$j60$l0$h0",
        "ac_session": "0tcpjiswj3j0em2ohbesy121pp0yy0vq",
        "sso_key": "a0f2901995cfc2f44aaa69ba8bdf3b6dcd8763487176941d10d077eac3f03bd9",
        "datadome": "6GQmiop5WCqnQqlTwvKa6l7cClRFz0EJL8tOHKKTk2uidgSuFVX9F~KPESDuBzK47hjmPJzr0fJJB24k1_5o6NgxLZe38u~upcN1s7SycNFAlMvPsnUFrZpiBgADi1PQ",
        "_ga": "GA1.1.1643681246.1749383929",
    }
    return jsonify(cookie)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
