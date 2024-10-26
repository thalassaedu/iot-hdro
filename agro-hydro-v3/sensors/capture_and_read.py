import cv2
import pytesseract
from flask import Flask, render_template_string, jsonify
from datetime import datetime

app = Flask(__name__)

# Template for the webpage
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Number Detection from Image</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { margin: 20px; }
        h2 { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Detected Numbers</h2>
        <p>Last Update: {{ timestamp }}</p>
        <pre>{{ numbers }}</pre>
        <button onclick="window.location.reload();">Refresh</button>
    </div>
</body>
</html>
"""

def capture_image():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    camera.release()
    if ret:
        # Save the image temporarily
        cv2.imwrite("captured_image.jpg", frame)
        return "captured_image.jpg"
    else:
        print("Failed to capture image.")
        return None

def extract_numbers_from_image(image_path):
    # Load the image
    img = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Use Tesseract to perform OCR on the image
    text = pytesseract.image_to_string(gray)
    
    # Extract numbers from the text
    numbers = [int(s) for s in text.split() if s.isdigit()]
    return numbers

@app.route('/')
def display_numbers():
    # Capture the image and read numbers
    image_path = capture_image()
    if image_path:
        numbers = extract_numbers_from_image(image_path)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return render_template_string(HTML_TEMPLATE, numbers=numbers, timestamp=timestamp)
    else:
        return "Failed to capture image."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
