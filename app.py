import os
import tempfile
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import base64
import io
from PIL import Image
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from inference_sdk import InferenceHTTPClient

load_dotenv()
app = Flask(__name__)
CORS(app)


client = InferenceClient(api_key="[API_Key]")

@app.route('/', methods=['GET', 'POST'])
def analyze_pest():
    try:
        if request.method == 'POST':
            file = request.files['file']

            # Save file to a temporary location
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, file.filename)
            file.save(temp_path)

            # Detect pest from saved image
            pest_result = detect_pest(temp_path)

            # Delete the temporary file after prediction
            os.remove(temp_path)

            if "error" in pest_result:
                return jsonify(pest_result), 500

            recommendations = get_ai_recommendations(pest_result['label'])
            image_base64 = encode_image_to_base64(file)
            return render_template("index.html", image_base64=image_base64, pest=pest_result['label'],
                                   confidence=f"{pest_result['score'] * 100:.1f}%", recommendations=recommendations)

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


def detect_pest(image_path):
    """Run inference on the saved image file"""
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="0YjWW9oyEX0rwncjLXbC"
    )

    # Pass the image path instead of bytes
    result = CLIENT.infer(image_path, model_id="kusk-ai-pest-detect-2n8qu/1")

    if 'predictions' in result and len(result['predictions']) > 0:
        insect_name = result['predictions'][0]['class']
        return {"label": insect_name, "score": result['predictions'][0]['confidence']}
    else:
        return {"error": "No pest detected"}


def get_ai_recommendations(pest):
    user_message = pest
    messages = [{"role": "system",
                 "content": "Generate a detailed description of an insect in exactly 5 lines. Each line should provide specific information about the insect, including its classification, physical characteristics, habitat, diet, behavior, and any unique adaptations. Ensure the description is informative, concise, and scientifically accurate."},
                {"role": "user", "content": "pest name is"+user_message}
                ]

    stream = client.chat.completions.create(
        model="microsoft/Phi-3.5-mini-instruct",
        messages=messages,
        temperature=0.5,
        max_tokens=2048,
        top_p=0.7,
        stream=True
    )
    ai_chat = ""
    for chunk in stream:
        ai_chat += chunk.choices[0].delta.content
    print(ai_chat)
    return ai_chat


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
