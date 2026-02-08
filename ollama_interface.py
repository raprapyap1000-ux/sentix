import ollama

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
        return [model['name'] for model in response['models']]
