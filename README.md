# AI Pest Control Advisor

## Overview
The **AI Pest Control Advisor** is a Flask-based web application that helps users identify pests from uploaded images and provides AI-generated recommendations for pest control. It utilizes Hugging Face's inference APIs for image classification and text generation.

## Features
- Upload an image to detect pests using a pre-trained ViT (Vision Transformer) model.
- Get AI-generated recommendations on identified pests.
- Responsive web interface.
- Implements Flask-CORS for cross-origin requests.
- Uses environment variables for secure API token handling.

## Technologies Used
- **Flask** (Python-based web framework)
- **Hugging Face Inference API** (Image recognition & AI text generation)
- **Flask-CORS** (Cross-Origin Resource Sharing)
- **PIL (Pillow)** (Image processing)
- **dotenv** (Environment variable management)
- **HTML & Jinja2** (Frontend rendering)

## Installation & Setup
### Prerequisites
Ensure you have Python 3.x installed.

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/ai-pest-control-advisor.git
   cd ai-pest-control-advisor
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root.
   - Add the following line, replacing `your_hf_token` with your actual Hugging Face API token:
     ```sh
     HF_TOKEN=your_hf_token
     ```

5. Run the Flask application:
   ```sh
   python app.py
   ```

6. Access the application in your browser:
   ```sh
   http://localhost:5002
   ```

## API Endpoints
### `GET /`
- Renders the homepage.

### `POST /`
- Accepts an image file for pest detection.
- Returns:
  - Pest label and confidence score.
  - AI-generated recommendations.

## Project Structure
```
/ai-pest-control-advisor
│── static/                # Static assets (CSS, JS, images)
│── templates/             # HTML templates
│── .env                   # Environment variables (ignored in Git)
│── app.py                 # Main Flask application
│── requirements.txt       # Python dependencies
│── README.md              # Documentation
```

## Future Enhancements
- Improve model accuracy with fine-tuned datasets.
- Implement a database to store pest data and user queries.
- Enhance UI with better styling and responsiveness.

## License
This project is open-source under the MIT License.

