import os
import cv2
import pytesseract
from PIL import Image

# Set the Tesseract executable path (Update this path as needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Administrador\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Define the path to your local directory with images
IMAGE_DIR = './Plates/'

# Check if the directory exists
if not os.path.isdir(IMAGE_DIR):
	print(f'Directory not found: {IMAGE_DIR}')
	exit()

# Iterate through all files in the directory
for filename in os.listdir(IMAGE_DIR):
	if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
		image_path = os.path.join(IMAGE_DIR, filename)
		print(f'Processing {image_path}...')
		try:
			# Read the image
			image = cv2.imread(image_path)
			# Convert the image to grayscale
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			# Apply Gaussian blur
			blur = cv2.GaussianBlur(gray, (5, 5), 0)
			# Edge detection
			edges = cv2.Canny(blur, 50, 200)
			# Find contours
			contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

			# Look for rectangular contours that could be a license plate
			for contour in contours:
				approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
				if len(approx) == 4:  # Selects only contours with 4 corners
					x, y, w, h = cv2.boundingRect(approx)
					roi = gray[y:y + h, x:x + w]
					# Use OCR to extract text
					plate_text = pytesseract.image_to_string(roi, config='--psm 8')
					plate_text = plate_text.strip()
					if plate_text:
						print(f'License Plate Detected: {plate_text}')
		except Exception as e:
			print(f'Error processing {image_path}: {e}')

print('Processing complete.')