import json
import subprocess

import requests


class ServerWrapper:
    def __init__(self, config=None):
        self.api_url = config.get("url") if config else "http://localhost:8080"

    def check_server(self):
        """Check the status of the sever."""
        response = requests.get(f"{self.api_url}/health")
        if response.status_code == 200:
            data = response.json()
            return {
                "status": data.get("status"),
                "slots_idle": data.get("slots_idle"),
                "slots_processing": data.get("slots_processing"),
            }
        else:
            return {
                "status": "error",
                "code": response.status_code,
                "message": response.text,
            }

    def tokenize(self, content):
        data = {"content": content}
        response = requests.post(
            f"{self.api_url}/tokenize",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
        )

        if response.status_code != 200:
            raise ValueError(f"Error from server while tokenizing: {response.text}")

        return response.json()

    def detokenize(self, tokens):
        data = {"tokens": tokens}
        response = requests.post(
            f"{self.api_url}/detokenize",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
        )

        if response.status_code != 200:
            raise ValueError(f"Error from server while detokenizing: {response.text}")

        return response.json()

    def generate_embedding(self, content, image_data=None):
        data = {"content": content, "image_data": image_data or []}

        response = requests.post(
            f"{self.api_url}/embedding",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
        )

        if response.status_code != 200:
            raise ValueError(f"Error from server: {response.text}")

        return response.json()

    def generate_completion(self, prompt, **kwargs):
        stream = False
        prompt = f"### Human: {prompt}\n### Assistant: "
        data = {
            "prompt": prompt,
            "temperature": kwargs.get("temperature", 0.8),
            "top_k": 40,
            "top_p": 0.9,
            "n_keep": 4,
            "n_predict": 128,
            "cache_prompt": True,
            "stop": ["\n### Human:"],
            "stream": stream,
            # ... add other parameters here, following the same pattern ...
        }

        # Add optional parameters only if they are explicitly provided
        for param in [
            "dynatemp_range",
            "dynatemp_exponent",
            "top_k",
            "top_p",
            "min_p",
            "n_predict",
            "n_keep",
            "stream",
            "stop",
            "tfs_z",
            "typical_p",
            "repeat_penalty",
            "repeat_last_n",
            "penalize_nl",
            "presence_penalty",
            "frequency_penalty",
            "penalty_prompt",
            "mirostat",
            "mirostat_tau",
            "mirostat_eta",
            "grammar",
            "seed",
            "ignore_eos",
            "logit_bias",
            "n_probs",
            "min_keep",
            "image_data",
            "slot_id",
            "cache_prompt",
            "system_prompt",
            "samplers",
        ]:
            if kwargs.get(param) is not None:
                data[param] = kwargs[param]

        # Send the POST request
        # print("Sending request: ", json.dumps(data))
        response = requests.post(
            f"{self.api_url}/completion",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
            stream=stream,
        )

        # Handle response
        if response.status_code != 200:
            raise ValueError(f"Error in chat completion: {response.text}")

        if not stream:
            return response.json()["content"]

        answer = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                if decoded_line.startswith("data: "):
                    json_content = decoded_line[len("data: ") :]
                    try:
                        data_segment = json.loads(json_content)
                        answer += data_segment.get("content", "")
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON segment: {json_content}")

        return answer.strip()

    def get_metrics(self):
        response = requests.get(f"{self.api_url}/metrics")

        if response.status_code != 200:
            raise ValueError(
                f"Error from server while fetching metrics: {response.text}"
            )

        # Metrics are typically returned in a text-based format that Prometheus can parse
        # Rather than JSON. Here, we simply return the raw text for further processing.
        return response.text


# Example usage
if __name__ == "__main__":
    server_wrapper = ServerWrapper({"url": "http://localhost:8080"})

    # Example usage for check server status
    print("Check server status: ", server_wrapper.check_server())

    # Example usage for completion
    completion_options = {
        "temperature": 0.7,
        "top_k": 50,
        # ... include other options as needed ...
    }
    prompt = "Building a website can be done in 10 simple steps:"
    completion = server_wrapper.generate_completion(prompt, **completion_options)
    print("Generate Completion: ", completion)

    # Example usage for embedding
    # content = "This is a sample text for which we want to generate an embedding."
    # image_data = [
    #     {
    #         "data": "base64_encoded_string_of_your_image",
    #         "id": 21
    #     }
    # ]
    # embedding = server_wrapper.generate_embedding(content, None)
    # print("Generate embedding: ", embedding)

    # Example usage for tokenization
    # content_to_tokenize = "Tokenize this text."
    # tokens = server_wrapper.tokenize(content_to_tokenize)
    # print("Generate Tokens: ", tokens)

    # # Example usage for detokenization
    # tokens_to_detokenize = tokens[
    #     "tokens"
    # ]  # assuming the token list is under 'tokens' key
    # text = server_wrapper.detokenize(tokens_to_detokenize)
    # print("Generate Detokenized text:", text)

    # # Examle usage for metrics
    # metrics = server_wrapper.get_metrics()
    # print(metrics)
