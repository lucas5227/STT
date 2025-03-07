from dotenv import load_dotenv
import os
from google import genai

class Gemini:
    def __init__(self):
        load_dotenv()
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))



    def summary(self, file_path):
        file = self.client.files.upload(file=file_path)
        print(f"{file=}")
        result = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[file, "\n\n", "이 음성로그를 요약해줘"]
            )
        self.client.files.delete(name=file.name)
    
        return result.text