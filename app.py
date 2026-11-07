from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    review = ""

    if request.method == "POST":

        code = request.form["code"]

        prompt = f"""
        You are a senior software engineer.

        Review the following code.

        Find:
        1. Syntax Errors
        2. Bugs
        3. Improvements
        4. Best Practices

        Code:

        {code}
        """

        try:
            response = client.models.generate_content(
                model="models/gemini-3.8-flash",
                contents=prompt
            )

            review = response.text

        except Exception as e:

            try:
                compile(code, "<string>", "exec")
                review = (
                    "No syntax errors found.\n\n"
                    "Gemini API is currently unavailable.\n"
                    f"Error: {e}"
                )

            except SyntaxError as se:
                review = f"Syntax Error Found:\n\n{se}"

    return render_template(
        "index.html",
        review=review
    )

if __name__ == "__main__":
    app.run(debug=True)