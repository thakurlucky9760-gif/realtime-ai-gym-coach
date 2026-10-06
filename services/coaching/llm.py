import os
from services.config.workout_config import PROMPT


class LLMCoach:
    def __init__(self, groq_client, model=None):
        self.client = groq_client
        self.history = []
        self.system_prompt = PROMPT
        self.model = model or os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")

    def give_feedback(self, event, issue):
        prompt = f"Event: {event}"

        if issue:
            prompt += f" Form Issue: {issue}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.history[-10:],
            {"role": "user", "content": prompt}
        ]

        candidate_models = [
            self.model,
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "qwen/qwen3.8-27b",
            "llama-3.3-70b-versatile",
        ]
        # Preserve order without duplicates
        candidate_models = list(dict.fromkeys([m for m in candidate_models if m]))

        for candidate in candidate_models:
            try:
                response = self.client.chat.completions.create(
                    model=candidate,
                    messages=messages,
                    temperature=0.4,
                )
                self.model = candidate
                text = response.choices[0].message.content.strip()
                self.history.append({"role": "assistant", "content": text})
                return text
            except Exception as e:
                continue

        if issue:
            return f"Keep going! Watch your form: {issue}"
        return "Keep pushing, stay strong!"

    