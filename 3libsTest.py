import cv2
import easyocr
from paddleocr import PaddleOCR

def ocr_paddleocr(image_path):
	ocr = PaddleOCR()
	result = ocr.ocr(image_path, cls=True)
	return ' '.join([line[1][0] for line in result[0] if line[1]])

def detect_license_plate(image_path):
	res = ocr_paddleocr(image_path)
	print("Detected License Plate Numbers:")
	print(res)
	return res

if __name__ == "__main__":
	image_path = "Plates/6381RM.png"  # Replace with your image path
	print(detect_license_plate(image_path))