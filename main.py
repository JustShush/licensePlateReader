import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from paddleocr import PaddleOCR
import tempfile
import asyncio

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
	return render_template("index.html")

async def run_ocr(image_path):
	# PaddleOCR is synchronous, so we run it in a thread
	ocr = PaddleOCR()
	loop = asyncio.get_event_loop()
	result = await loop.run_in_executor(
		None,  # Uses default ThreadPoolExecutor
		lambda: ocr.ocr(image_path, cls=True))
	return ' '.join([line[1][0] for line in result[0] if line[1]])

@app.route('/process_image', methods=['POST'])
async def process_image():
	if 'image' not in request.files:
		return jsonify({"error": "No image file"}), 400
		
	file = request.files['image']
	temp_path = None

	try:
		# Save to temp file (synchronous but fast)
		with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
			file.save(tmp.name)
			temp_path = tmp.name

		# Process with async OCR
		plate_text = await run_ocr(temp_path)
		return jsonify({"plate": plate_text})

	except Exception as e:
		return jsonify({"error": str(e)}), 500

	finally:
		# Clean up temp file
		if temp_path and os.path.exists(temp_path):
			os.remove(temp_path)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)