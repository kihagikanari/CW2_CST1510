import google.generativeai as genai

class AIassistant:
    def __init__(self):
        self.api_key = "AIzaSyBcoEWOZ0mdTC-lXoyDxqtmoDPFKKZtjzY"
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-flash-latest")
            self.is_working = True
        except Exception as e:
            self.is_working = False
            self.error = str(e)

    def get_ai_insight(self, prompt):
        #ai analysis
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI service error: {str(e)}"

ai_assistant = AIassistant()