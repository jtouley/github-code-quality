import os
from openai import OpenAI
from src.config_loader import load_config  # ✅ Added config loader import


class AIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment.")
        # Create the OpenAI client inside the __init__ method.
        self.client = OpenAI(api_key=self.api_key)

    def generate_prompt(self, code):
        """Constructs an OpenAI prompt dynamically based on YAML configuration."""
        config = load_config()
        dry_weight = config.get("analysis", {}).get("dry", {}).get("weight", 0.5)
        solid_weight = config.get("analysis", {}).get("solid", {}).get("weight", 0.5)
        solid_priorities = [
            p
            for p, v in config.get("analysis", {})
            .get("solid", {})
            .get("principles", {})
            .items()
            if v.get("enabled", False)
        ]

        prompt = (
            "Analyze the given Python code based on DRY and SOLID principles.\n\n"
            f"**DRY Analysis:** Focus {dry_weight*100}% on DRY principles. Identify redundant patterns, "
            "unnecessary repetition, and opportunities for logic reuse.\n\n"
            f"**SOLID Analysis:** Focus {solid_weight*100}% on SOLID principles. Prioritize {', '.join(solid_priorities)}. "
            "Evaluate adherence to these principles and suggest improvements.\n\n"
            "For each category, assign a **score from 1 to 10**, where 1 is poor adherence and 10 is excellent adherence.\n\n"
            f"Code:\n{code}\n\n"
            "### Response Format (Example Output):\n"
            "### DRY Analysis\n**Score: 7/10**\n**Summary:** <your analysis>\n\n"
            "### SOLID Analysis\n**Score: 5/10**\n**Summary:** <your analysis>"
        )

        return prompt

    def analyze_code(self, code):
        """Analyzes the given code using OpenAI for DRY & SOLID principles."""
        prompt = self.generate_prompt(code)  # ✅ Updated to use dynamic prompt

        try:
            config = load_config()
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=config.get("prompt_customization", {}).get(
                    "temperature", 0.3
                ),  # ✅ Uses YAML config
                max_tokens=config.get("prompt_customization", {}).get(
                    "max_tokens", 500
                ),  # ✅ Uses YAML config
            )
            return response.choices[0].message.content
        except Exception as e:
            return (
                f"Error analyzing code: {str(e)}\n\n"
                "To resolve this, either run `openai migrate` to update your codebase to the new API "
                "or pin your installation to an older version, e.g., `pip install openai==0.28`."
            )
