class ChatModel:
    def __init__(self, instruction):
        self.instruction = instruction
        self.chat_history = []

    def format_chat_prompt(self, user_input):
        formatted_chat = f"{self.instruction}\n"
        for i, message in enumerate(self.chat_history):
            speaker = "Human" if i % 2 == 0 else "Assistant"
            formatted_chat += f"### {speaker}: {message}\n"
        formatted_chat += f"### Human: {user_input}\n### Assistant: "
        return formatted_chat
    
    def format_prompt(self, user_input):
        formatted_chat = f"{self.instruction}\n"
        formatted_chat += f"### Human: {user_input}\n### Assistant: "
        return formatted_chat
