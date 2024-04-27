#!/usr/bin/python3
""" creates a flask app """
from flask import Flask

app = Flask(__name__)

# Register index_bp
app.register_blueprint(idex_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
