import asyncio
import ollama
from sentix_core.agent import Agent
from ollama_interface import OllamaInterface

async def main():
    print("Sentix: Local-first, Security-Focused AI Agent")
    print("Initializing Ollama interface...")
    ollama_host = "http://localhost:11434"
    ollama_model = input("enter model:") # Default model, can be configured later

    ollama_interface = OllamaInterface(host=ollama_host, model=ollama_model)

    try:
        # Verify Ollama server and model availability
        available_models = await ollama_interface.list_models()
        print(f"Available Ollama models: {', '.join(available_models)}")
        if ollama_model not in [m['name'] for m in available_models]:
            print(f"Error: Default model '{ollama_model}' not found. Please pull it using 'ollama pull {ollama_model}' and restart Sentix.")
            return

    except ollama.ResponseError as e:
        print(f"Error connecting to Ollama server at {ollama_host}: {e}. Please ensure Ollama is running.")
        return
    except ollama.ClientError as e:
        print(f"An Ollama client error occurred: {e}. Please check your Ollama setup.")
        return
    except Exception as e:
        print(f"An unexpected error occurred during Ollama initialization: {e}")
        return

    agent = Agent(ollama_interface)

    print("Sentix agent is ready. Type 'exit' or 'quit' to stop.")

    while True:
        user_input = input("You > ")
        if user_input.lower() in ['exit', 'quit']:
            break

        observation = await agent.observe(user_input)
        reasoning = await agent.reason(observation)
        print(f"Agent Reasoning: {reasoning}")
        
        # Simple action execution for now, will be replaced by a more robust system
        if reasoning.startswith("exec(") or \
           reasoning.startswith("read_file(") or \
           reasoning.startswith("write_file(") or \
           reasoning.startswith("edit_file("):
            action_result = await agent.act(reasoning)
            print(f"Agent Action Result: {action_result}")

if __name__ == "__main__":
    asyncio.run(main())
