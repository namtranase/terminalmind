class AssistantGit:
    def __init__(self) -> None:
        pass
    
    def get_response(self, api_func, user_input):
        completion_options = {
            "temperature": 0.7,
            "top_k": 50,
            "n_predict": 128,
            # ... include other options as needed ...
        }
        prompt = f"### Human: {user_input}\n### Assistant: "
        response = api_func(prompt, **completion_options)
        
        return response
        
    
class AssistantTerminal:
    def __init__(self) -> None:
        pass
    
    def get_response(self, api_func, user_input):
        completion_options = {
            "temperature": 0.7,
            "top_k": 50,
            "n_predict": 128,
            # ... include other options as needed ...
        }
        prompt = f"### Human: {user_input}\n### Assistant: "
        response = api_func(prompt, **completion_options)
        
        return response