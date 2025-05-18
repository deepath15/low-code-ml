import os

import google.generativeai as genai



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


