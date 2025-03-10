import os
from openai import OpenAI
from src.config_loader import load_config
from src.utils import log


class AIClientConfig:
    """Handles AI client configuration and prompt generation."""

    def __init__(self):
        self.config = load_config()

    def get_model_settings(self):
        """Returns OpenAI model settings from config."""
        return {
            "model": "gpt-4o-mini",
            "temperature": self.config.get("prompt_customization", {}).get(
                "temperature", 0.3
            ),
            "max_tokens": self.config.get("prompt_customization", {}).get(
                "max_tokens", 500
            ),
        }

    def get_analysis_weights(self):
        """Returns the weights for DRY and SOLID analysis."""
        dry_weight = self.config.get("analysis", {}).get("dry", {}).get("weight", 0.5)
        solid_weight = (
            self.config.get("analysis", {}).get("solid", {}).get("weight", 0.5)
        )
        return {"dry_weight": dry_weight, "solid_weight": solid_weight}

    def get_solid_priorities(self):
        """Returns enabled SOLID principles from config."""
        return [
            p
            for p, v in self.config.get("analysis", {})
            .get("solid", {})
            .get("principles", {})
            .items()
            if v.get("enabled", False)
        ]


class PromptGenerator:
    """Responsible for generating analysis prompts."""

    def __init__(self, config):
        self.config = config

    def generate_code_analysis_prompt(self, code):
        """Constructs an OpenAI prompt dynamically based on YAML configuration."""
        weights = self.config.get_analysis_weights()
        priorities = self.config.get_solid_priorities()

        prompt = (
            "Analyze the given Python code based on DRY and SOLID principles.\n\n"
            f"**DRY Analysis:** Focus {weights['dry_weight']*100}% on DRY principles. Identify redundant patterns, "
            "unnecessary repetition, and opportunities for logic reuse.\n\n"
            f"**SOLID Analysis:** Focus {weights['solid_weight']*100}% on SOLID principles. Prioritize {', '.join(priorities)}. "
            "Evaluate adherence to these principles and suggest improvements.\n\n"
            "For each category, assign a **score from 1 to 10**, where 1 is poor adherence and 10 is excellent adherence.\n\n"
            f"Code:\n{code}\n\n"
            "### Response Format (Example Output):\n"
            "### DRY Analysis\n**Score: 7/10**\n**Summary:** <your analysis>\n\n"
            "### SOLID Analysis\n**Score: 5/10**\n**Summary:** <your analysis>"
        )

        return prompt


class AIClient:
    """Client for interacting with OpenAI API for code analysis."""

    def __init__(self):
        self.api_key = self._validate_api_key()
        self.client = OpenAI(api_key=self.api_key)
        self.config = AIClientConfig()
        self.prompt_generator = PromptGenerator(self.config)

    def _validate_api_key(self):
        """Validates that the OpenAI API key is available."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment.")
        return api_key

    def analyze_code(self, code):
        """Analyzes the given code using OpenAI for DRY & SOLID principles."""
        prompt = self.prompt_generator.generate_code_analysis_prompt(code)

        try:
            model_settings = self.config.get_model_settings()
            response = self.client.chat.completions.create(
                model=model_settings["model"],
                messages=[{"role": "user", "content": prompt}],
                temperature=model_settings["temperature"],
                max_tokens=model_settings["max_tokens"],
            )
            return response.choices[0].message.content
        except Exception as e:
            error_message = (
                f"Error analyzing code: {str(e)}\n\n"
                "To resolve this, either run `openai migrate` to update your codebase to the new API "
                "or pin your installation to an older version, e.g., `pip install openai==0.28`."
            )
            log(error_message)
            return error_message
