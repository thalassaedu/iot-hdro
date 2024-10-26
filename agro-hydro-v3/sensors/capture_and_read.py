import cv2
import pytesseract
import base64
from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

# HTML template for the webpage
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Number Detection from Image</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        .container { margin: 20px; }
        h2 { color: #333; }
        img { max-width: 100%; height: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Detected Numbers</h2>
        <p>Last Update: {{ timestamp }}</p>
        <pre>{{ numbers }}</pre>
        <h3>Captured Image</h3>
        <img src="data:image/jpg;base64,{{ image_data }}" alt="Captured Image">
        <br>
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

def preprocess_image(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Resize the image to make the text clearer
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding to highlight the text
    processed_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    return processed_img

def extract_numbers_from_image(image_path):
    # Preprocess the image
    processed_img = preprocess_image(image_path)

    # Use Tesseract to perform OCR on the processed image
    text = pytesseract.image_to_string(processed_img)

    # Extract numbers from the text
    numbers = [int(s) for s in text.split() if s.isdigit()]
    return numbers

def encode_image_to_base64(image_path):
    # Read the image and encode it as base64
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_image

@app.route('/')
def display_numbers():
    # Capture the image and read numbers
    image_path = capture_image()
    if image_path:
        numbers = extract_numbers_from_image(image_path)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        image_data = encode_image_to_base64(image_path)
        return render_template_string(HTML_TEMPLATE, numbers=numbers, timestamp=timestamp, image_data=image_data)
    else:
        return "Failed to capture image."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)