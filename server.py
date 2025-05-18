import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
from htmlToCode import convert_html_css_to_react
from imageToCode import generate_code_from_image
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://low-code.deepath.tech"}})

GOOGLE_API_KEY ="AIzaSyAtzayC90UMhnnROSxOQA1w9nWxZtK37Sk"
genai.configure(api_key=GOOGLE_API_KEY)

def convert_html_css_to_react(html_code, css_code):
    prompt = f"""Convert the following HTML and CSS into a React functional component using Tailwind CSS.
    - The component should be named MyComponent.
    - Ensure that the output includes export default MyComponent; at the end.
    - Return only the React code without any markdown code fences (```jsx) or additional explanations.

    HTML Input:
    {html_code}
    
    CSS Input:
    {css_code}

    Output:
    A complete React functional component named MyComponent, with Tailwind CSS classes, and ending with export default MyComponent;.
    """

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  
        response = model.generate_content(prompt)
        return response.text 
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/convert', methods=['POST'])
def convert():
    print("Received request to convert HTML and CSS to React component")
    data = request.json
    html_code = data.get("html", "")
    css_code = data.get("css", "")
    print(f"Received HTML: {html_code}")

    if not html_code or not css_code:
        return jsonify({"error": "HTML and CSS are required"}), 400 
    print(f"Received CSS: {css_code}")
    react_code = convert_html_css_to_react(html_code, css_code)
    print(react_code)
    return jsonify({"component": react_code})


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

if __name__ == '__main__':
    print("🚀 Server is running on port 5000")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

