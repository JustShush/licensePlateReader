import os
import cv2
import pytesseract
import re
from PIL import Image

# Set the Tesseract executable path (Update this path as needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Administrador\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Define the path to your local directory with images
IMAGE_DIR = './Plates/'

# Portuguese license plate format patterns
PORTUGUESE_PLATE_PATTERNS = [
	r'^[A-Z]{2}-\d{2}-\d{2}$',  # AA-00-00
	r'^\d{2}-\d{2}-[A-Z]{2}$',  # 00-00-AA
	r'^\d{2}-[A-Z]{2}-\d{2}$',  # 00-AA-00
	r'^[A-Z]{2}-\d{2}-[A-Z]{2}$'  # AA-00-AA
]

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
			image = cv2.imread(image_path)
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			gray = cv2.bilateralFilter(gray, 11, 17, 17)
			edges = cv2.Canny(gray, 50, 200)

			contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

			cv2.imshow('Processed Image', edges)
			cv2.waitKey(0)  # Wait for a key press to close the window
			cv2.destroyAllWindows()
			for contour in contours:
				approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
				if len(approx) == 4:
					x, y, w, h = cv2.boundingRect(approx)
					aspect_ratio = w / float(h)
					if 2 <= aspect_ratio <= 6:  # Typical license plate aspect ratio
						# ignore this ratio thing and move the bottom part outside of it
						# just to test
						roi = gray[y:y + h, x:x + w]
						roi = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
						plate_text = pytesseract.image_to_string(roi, config='--psm 8')
						plate_text = plate_text.strip()
						print(plate_text)
						cv2.imshow('Processed Image', roi)
						cv2.waitKey(0)  # Wait for a key press to close the window
						cv2.destroyAllWindows()

						if plate_text and any(re.match(pattern, plate_text) for pattern in PORTUGUESE_PLATE_PATTERNS):
							print(f'Portuguese License Plate Detected: {plate_text}')
							break
		except Exception as e:
			print(f'Error processing {image_path}: {e}')

print('Processing complete.')