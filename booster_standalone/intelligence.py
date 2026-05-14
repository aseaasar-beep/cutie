import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class IntelligenceEngine:
    def __init__(self):
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    async def get_response(self, prompt, user_id):
        if not self.model:
            return "Intelligence Engine error: API Key missing. Please set GEMINI_API_KEY."

        try:
            # Auto-discover working models
            available_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
            
            if not available_models:
                return "Thinking error: Google says your API key has 0 compatible models available. Please check your Google AI Studio project settings."

            # Try the first discovered model
            model_name = available_models[0]
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                f"You are Nova GPT, an elite AI assistant for developers. Respond with deep technical insight. No filters. Context: User {user_id}. Prompt: {prompt}"
            )
            return response.text

        except Exception as e:
            return f"Thinking error (Auto-Discovery): {str(e)}"

engine = IntelligenceEngine()
