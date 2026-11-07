from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

try:
    response = client.models.generate_content(
        model="models/gemini-3.8-flash",
        contents="Say Hello"
    )

    print(response.text)

except Exception as e:
    print("Error:", e)