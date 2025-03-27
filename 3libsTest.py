import cv2
import pytesseract
import easyocr
from paddleocr import PaddleOCR
import numpy as np

# Configure Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Administrador\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
	image = cv2.imread(image_path)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	return gray

def ocr_pytesseract(image):
	return pytesseract.image_to_string(image, config='--psm 8')

def ocr_easyocr(image_path):
	reader = easyocr.Reader(['en'])
	result = reader.readtext(image_path)
	return ' '.join([text[1] for text in result])

def ocr_paddleocr(image_path):
	ocr = PaddleOCR()
	result = ocr.ocr(image_path, cls=True)
	return ' '.join([line[1][0] for line in result[0] if line[1]])

def combine_results(results):
	merged_results = []
	for text in results:
		if text and text not in merged_results:
			merged_results.append(text)
	return merged_results

def detect_license_plate(image_path):
	#processed_image = preprocess_image(image_path)

	#text1 = ocr_pytesseract(processed_image)
	#text2 = ocr_easyocr(image_path)
	text3 = ocr_paddleocr(image_path)

	# nem e preciso usar as outras duas libs, esta paddleOCR e TOP
	combined_output = combine_results([text3]) # text1, text2, text3

	print("Detected License Plate Numbers:")
	for text in combined_output:
		print(text)

if __name__ == "__main__":
	image_path = "Plates/6381RM.png"  # Replace with your image path
	detect_license_plate(image_path)