import json
import os
import time
from datetime import datetime
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

import praw


class RedditNews:
    def __init__(self, config, update_time, channel) -> None:
        self.config = config
        self.reddit = self.load_instance(config)
        self.update_time = update_time * 60  # Convert to seconds
        self.channels = channel
        self.top = config["criteria"].get("top", 5)
        self.score = config["criteria"].get("score", 5)
        self.comments_limit = config["criteria"].get("comment_limit", 5)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.base_dir = "data"
        
    def load_instance(self, config):
        reddit = praw.Reddit(
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            user_agent=config["user_agent"],
        )
        return reddit
    
    # For get the context
    def get_context(self, question, text):
        documents = self.text_splitter.split_text(text)
        db = Chroma.from_texts(documents, embedding=self.embeddings)
        retriever = db.as_retriever(search_kwargs={"k": 3})
        context = retriever.get_relevant_documents(question)
        
        return context
    
    def get_content(self, channel):
        file_path = os.path.join(self.base_dir, f"{channel}.json")
        data_text = ""
        with open(file_path, "r") as f:
            data = json.load(f)
        for news in data:
            # comments = "---".join([cmt for cmt in news["top_comments"]])
            # data_text += news["title"] + "-" + news["content"] + "--" + comments + "\n"
            data_text += news["title"] + "-" + news["content"] + "\n"
            
        return data_text

    # For get the raw data
    def get_data(self):
        data = {}
        for channel in self.channels:
            subreddit = self.reddit.subreddit(channel)
            posts = subreddit.hot(limit=self.top)
            channel_data = []
            for post in posts:
                post.comments.sort = "top"
                post.comments.replace_more(limit=0)  # Fetch all top-level comments
                comments = [
                    comment.body
                    for comment in post.comments.list()[: self.comments_limit]
                ]

                post_data = {
                    "id": post.id,
                    "title": post.title,
                    "url": post.url,
                    "created_utc": post.created_utc,
                    "content": post.selftext,
                    "top_comments": comments,
                }
                channel_data.append(post_data)
            data[channel] = channel_data
        return data

    def update_data(self):
        new_data = self.get_data()
        # For simplicity, this example directly calls save_data
        self.save_data(new_data)

    def save_data(self, data):
        base_dir = self.base_dir
        max_elements = 100  # Maximum number of posts per file
        os.makedirs(base_dir, exist_ok=True)
        
        for channel, new_posts in data.items():
            file_path = os.path.join(base_dir, f"{channel}.json")
            
            # Load existing data if file exists
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    existing_posts = json.load(file)
            else:
                existing_posts = []
            
            # Update existing data with new posts, checking for duplicates
            existing_ids = {post['id'] for post in existing_posts}
            updated_posts = existing_posts.copy()
            
            for post in new_posts:
                if post['id'] not in existing_ids:
                    updated_posts.append(post)
                    existing_ids.add(post['id'])
            
            # If the updated list exceeds the maximum elements, trim the oldest
            if len(updated_posts) > max_elements:
                updated_posts = updated_posts[-max_elements:]
            
            # Save updated data
            with open(file_path, "w") as file:
                json.dump(updated_posts, file, indent=2)

    def cron_fetch_posts(self):
        last_run = 0
        while True:
            current_time = time.time()
            if current_time - last_run > self.update_time:
                print("Fetching new data...")
                self.update_data()
                print("Data updated.")
                last_run = current_time
            time.sleep(60)  # Check every 60 seconds           
    

def main():
    config = json.load(open("playground/reddit_config.json"))
    update_time = 1  # min
    channel = ["LocalLLama"]
    

    reddit_news = RedditNews(config, update_time, channel)
    reddit_news.cron_fetch_posts()
    

if __name__ == "__main__":
    main()
    
