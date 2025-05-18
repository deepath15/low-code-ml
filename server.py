import os

from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://low-code.deepath.tech"}})
  # Allow cross-origin requests

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

if __name__ == '__main__':
    print("🚀 Server is running on port 5000")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

