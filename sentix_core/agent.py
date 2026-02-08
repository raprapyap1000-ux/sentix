import asyncio
import subprocess
import os

class Agent:
    def __init__(self, ollama_interface):
        self.ollama_interface = ollama_interface
        self.memory = []
        self.tools = {}

    async def observe(self, prompt):
        # Simulate observation based on prompt (e.g., read files, check system status)
        return f"Observed: {prompt}"

    async def reason(self, observation):
        # Use Ollama to reason about the observation and decide on an action
        system_prompt = "You are a security-focused AI agent. Analyze the observation and propose a secure action. If a tool is needed, specify it.\n\nAvailable Tools:\n- exec(command): Execute a shell command securely.\n- read_file(path): Read a file securely.\n- write_file(path, content): Write content to a file securely.\n- edit_file(path, old_text, new_text): Edit a file securely.\n"
        user_message = f"Observation: {observation}\n\nBased on this, what is the most secure and appropriate action?"
        response = await self.ollama_interface.chat(system_prompt, user_message)
        return response

    async def act(self, action_plan):
        # Execute the chosen action. This is where security checks are crucial.
        if action_plan.startswith("exec("):
            command = action_plan[len("exec("): -1]
            print(f"Executing (securely): {command}")
            try:
                # WARNING: This is a basic implementation. For a security-focused agent,
                #          proper sandboxing (e.g., Docker, nsjail) and permission checks are CRUCIAL.
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                output = stdout.decode().strip()
                error = stderr.decode().strip()
                if process.returncode != 0:
                    return f"Error executing command: {error or output}"
                return f"Command output: {output}"
            except Exception as e:
                return f"Exception during command execution: {e}"
        elif action_plan.startswith("read_file("):
            path = action_plan[len("read_file("): -1]
            print(f"Reading (securely): {path}")
            try:
                with open(path, 'r') as f:
                    content = f.read()
                return f"File content: {content}"
            except FileNotFoundError:
                return f"Error: File not found at {path}"
            except Exception as e:
                return f"Error reading file {path}: {e}"
        elif action_plan.startswith("write_file("):
            parts = action_plan[len("write_file("): -1].split(',', 1)
            if len(parts) < 2:
                return "Error: write_file requires both path and content."
            path = parts[0].strip()
            content = parts[1].strip().strip('\'\"') # Remove quotes from content
            print(f"Writing (securely): {path} with content {content}")
            try:
                with open(path, 'w') as f:
                    f.write(content)
                return f"Successfully wrote to: {path}"
            except Exception as e:
                return f"Error writing to file {path}: {e}"
        elif action_plan.startswith("edit_file("):
            parts = action_plan[len("edit_file("): -1].split(',', 2)
            if len(parts) < 3:
                return "Error: edit_file requires path, old_text, and new_text."
            path = parts[0].strip()
            old_text = parts[1].strip().strip('\'\"')
            new_text = parts[2].strip().strip('\'\"')
            print(f"Editing (securely): {path}, replacing '{old_text}' with '{new_text}'")
            try:
                with open(path, 'r') as f:
                    content = f.read()
                if old_text not in content:
                    return f"Error: Old text '{old_text}' not found in file {path}"
                new_content = content.replace(old_text, new_text, 1)
                with open(path, 'w') as f:
                    f.write(new_content)
                return f"Successfully edited: {path}"
            except FileNotFoundError:
                return f"Error: File not found at {path}"
            except Exception as e:
                return f"Error editing file {path}: {e}"
        else:
            return f"Unhandled action: {action_plan}"

    def add_tool(self, name, func):
        self.tools[name] = func
