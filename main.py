import os
from flask import Flask, request, render_template, jsonify, url_for, send_file, redirect
from flask_cors import CORS
import cv2
import numpy as np
import pytesseract

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (for frontend)

# C:\Users\Administrador\AppData\Local\Programs\Tesseract-OCR

@app.route('/')
def main():
	return render_template("index.html")

def process_license_plate(image):
	# Convert image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Apply edge detection
	edged = cv2.Canny(gray, 100, 200)

	# Find contours
	contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# Loop through contours to find potential plates
	for cnt in contours:
		x, y, w, h = cv2.boundingRect(cnt)
		aspect_ratio = w / h
		if 2 < aspect_ratio < 5:  # Typical aspect ratio of a license plate
			plate_img = gray[y:y+h, x:x+w]
			text = pytesseract.image_to_string(plate_img, config='--psm 7')  # OCR
			return text.strip()

	return "No plate detected"

@app.route('/process_image', methods=['POST'])
def process_image():
	file = request.files['image']
	npimg = np.frombuffer(file.read(), np.uint8)
	image = cv2.imdecode(npimg, cv2.IMREAD_COLOR) 

	plate_text = process_license_plate(image)
	return jsonify({"plate": plate_text})

if __name__ == "__main__":
	app.run(host="127.0.0.1", debug=True, port=5000)