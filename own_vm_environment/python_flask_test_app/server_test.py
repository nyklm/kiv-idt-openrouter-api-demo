from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    value = request.args.get("value", "nic nebylo zadáno")
    return f"""
    <html>
        <head>
            <title>Flask GET demo</title>
        </head>
        <body>
            <h1>GET parametr</h1>
            <p>Hodnota parametru <b>value</b>:</p>
            <h2>{escape(value)}</h2>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)