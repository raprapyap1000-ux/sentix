import ollama
import ollama.exceptions

class OllamaInterface:
    def __init__(self, host="http://localhost:11434", model="llama2"):
        self.host = host
        self.model = model
        self.client = ollama.AsyncClient(host=self.host)

    async def chat(self, system_prompt, user_message):
        response = await self.client.chat(
            model=self.model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_message}
            ],
            stream=False
        )
        return response['message']['content']

    async def list_models(self):
        response = await self.client.list()
        # Safely get 'models' key, default to empty list if not present
        # Each item in the 'models' list is expected to be a dictionary
        # with a 'name' key. Using .get() for robustness.
        return [model.get('name') for model in response.get('models', []) if model.get('name')]
