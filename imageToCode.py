from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import google.generativeai as genai

import os
# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
# Allow cross-origin requests

# Configure Gemini API
genai.configure(api_key="AIzaSyAtzayC90UMhnnROSxOQA1w9nWxZtK37Sk")

# Function to generate code from image using Gemini
def generate_code_from_image(image_base64):
    try:
        image_bytes = base64.b64decode(image_base64)
        image = {
            "mime_type": "image/png",
            "data": image_bytes
        }

        prompt = """
        Convert this UI image into a clean and modern React component using JSX and Tailwind CSS.
        Match the layout, colors, and spacing.
        Only return JSX code without any additional comments or markers.
        """

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([prompt, image])
        # Clean the response
        generated_code = response.text
        cleaned_code = generated_code.replace("```jsx", "").replace("```", "").strip()
        cleaned_code = cleaned_code.replace("{/* Add content here if needed */}", "").strip()
        cleaned_code = cleaned_code.replace("{/", "").replace("/}", "").strip()

        return cleaned_code

    except Exception as e:
        print(f"Error in generate_code_from_image: {e}")
        return None

# POST endpoint to receive image and return code
@app.route('/generate-code', methods=['POST'])
def generate_code():
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'Missing image data'}), 400

        image_data = data['image'].split(',')[1]  # Remove "data:image/png;base64," part
        generated_code = generate_code_from_image(image_data)

        if generated_code is None:
            return jsonify({'error': 'Failed to generate code'}), 500

        return jsonify({'component': generated_code})

    except Exception as e:
        print(f"Error in /generate-code: {e}")
        return jsonify({'error': str(e)}), 500

# Run the server
if __name__ == '__main__':
    print("🚀 Server is running on port 8000")
    app.run(debug=True, port=8000)
