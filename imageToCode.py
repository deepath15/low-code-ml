
import base64
import google.generativeai as genai




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
