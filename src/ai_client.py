import os
from openai import OpenAI


class AIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment.")
        # Create the OpenAI client inside the __init__ method.
        self.client = OpenAI(api_key=self.api_key)

    def analyze_code(self, code):
        """Analyzes the given code using OpenAI for DRY & SOLID principles."""
        prompt = (
            "Analyze the following Python code and provide a score based on DRY and SOLID principles. "
            "Output a score between 1 and 10 for DRY and SOLID, also include a brief summary for both. "
            "Keep your response concise (under 50 words total) and to the point.\n\n"
            f"{code}"
        )
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            return (
                f"Error analyzing code: {str(e)}\n\n"
                "To resolve this, either run `openai migrate` to update your codebase to the new API "
                "or pin your installation to an older version, e.g., `pip install openai==0.28`."
            )
