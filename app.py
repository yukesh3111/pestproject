from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os
import base64
import io
from PIL import Image
from dotenv import load_dotenv
import time

load_dotenv()
app = Flask(__name__)
CORS(app)

HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}


@app.route('/', methods=['GET','POST'])
def analyze_pest():
    try:
        if(request.method == 'POST'):
            # Detect pest from image
            file = request.files['file']
            image_data = file.read()
            pest_result = detect_pest(image_data)
            if "error" in pest_result:
                return jsonify(pest_result), 500
            # Get AI recommendations
            recommendations = get_ai_recommendations(pest_result['label'])
            image_base64 = encode_image_to_base64(file)
            return render_template("index.html", image_base64=image_base64,pest=pest_result['label'], confidence=f"{pest_result['score']*100:.1f}%", recommendations = recommendations )
        return render_template("index.html")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def encode_image_to_base64(image_file):
    """Convert image file to Base64 format"""
    img = Image.open(image_file)
    img = img.convert("RGB")  # Ensure image is in RGB mode

    buffered = io.BytesIO()
    img.save(buffered, format="PNG")  # Save as PNG
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str
def detect_pest(image_data):
    API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"

    for _ in range(3):  # Retry logic
        response = requests.post(API_URL, headers=HEADERS, data=image_data)
        if response.status_code == 200:
            return response.json()[0]
        time.sleep(15)
    return {"error": "Pest detection failed"}

def get_ai_recommendations(pest):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

    prompt = f""" discription of {pest} insect"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 500,
            "temperature": 0.7,
            "do_sample": True,
            "top_p": 0.9,
            "repetition_penalty": 1.2
        }
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            full_response = response.json()[0]['generated_text']

            # Enhanced response cleaning
            clean_response = full_response.split("**Structure:**")[-1] \
                .split("\n\nNote:")[0] \
                .replace(prompt, "") \
                .strip()

            return clean_response.replace("\n", "<br>")
        return "Recommendations being generated..."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)