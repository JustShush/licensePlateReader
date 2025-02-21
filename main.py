import os
from flask import Flask, request, render_template, jsonify, url_for, send_file, redirect

app = Flask(__name__)

@app.route('/')
def main():
	return render_template("index.html")

if __name__ == "__main__":
	app.run(debug=True, port=5000)