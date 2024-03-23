from .fetch_news import RedditNews

class AssistantReddit:
    def __init__(self, config, channel) -> None:
        self.reddit_news = RedditNews(config=config, update_time=60, channel=channel)
        # self.reddit_news.cron_fetch_posts()
        
    def get_response(self, api_func, user_input, channel):
        completion_options = {
            "temperature": 0.7,
            "top_k": 50,
            "n_predict": 128,
            # ... include other options as needed ...
        }
        full_text = self.reddit_news.get_content(channel)
        
        if "summary" in user_input.lower():
            return full_text

        context = self.reddit_news.get_context(user_input, full_text)
        prompt = f"""Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Answer only factual information based on the context.
        Context: {context}.\n
        Question: {user_input}
        Helpful Answer:"""
        response = api_func(prompt, **completion_options)
        return response