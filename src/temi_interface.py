import argparse
import json

from .modules.assistant.assistant import AssistantGit, AssistantTerminal
from .modules.redditnews.assistant import AssistantReddit
from .modules.function_calling.function_model import TermFuncCall
from .modules.redditnews.fetch_news import RedditNews
from .prompt_wrapper import PromptWrapper
from .server_wrapper import ServerWrapper

class TemiInterface:
    def __init__(self, server_config_path="configs/server_config.json", reddit_config_path="playground/reddit_config.json"):
        config = None
        with open(server_config_path, "r", encoding="utf-8") as config_file:
            server_config = json.load(config_file)
        with open(reddit_config_path, "r", encoding="utf-8") as config_file:
            reddit_config = json.load(config_file)

        self.server_wrapper = ServerWrapper(config=server_config)
        self.prompt_wrapper = PromptWrapper()
        self.ast_terminal = AssistantTerminal
        self.ast_git = AssistantGit
        
        self.default_channel = "LocalLLama"
        self.ast_reddit = AssistantReddit(config=reddit_config, channel=self.default_channel)

        self.term_func = TermFuncCall

    def check_server_status(self):
        status = self.server_wrapper.check_server()
        return status

    def handle_assitant(self, user_input):
        if "git" in user_input:
            return self.ast_git.get_response(
                self.server_wrapper.generate_completion, user_input
            )
        else:
            return self.ast_terminal.get_response(
                self.server_wrapper.generate_completion, user_input
            )
            
    def handle_reddit_news(self, user_input):
        return self.ast_reddit.get_response(
            self.server_wrapper.generate_completion, user_input, self.default_channel)

def main():
    parser = argparse.ArgumentParser(description="temi - Your Terminal Assistant")
    subparsers = parser.add_subparsers(dest="command")

    # Parser for "check server" command
    server_parser = subparsers.add_parser("check", help="Check the temi server status")
    server_parser.add_argument(
        "status", nargs="?", help='The "status" argument to check the server'
    )

    # Parser for "assistant" command
    query_parser = subparsers.add_parser("assistant", help="Assistant mode")
    query_parser = subparsers.add_parser("reddit", help="Assistant mode")
    query_parser.add_argument(
        "user_input", nargs="+", help="The question or command for temi to process"
    )

    args = parser.parse_args()
    temi_interface = TemiInterface("configs/sevrer_config.json")

    if args.command == "check":
        status = temi_interface.check_server_status()
        print(status)
    elif args.command == "assistant":
        # Join the list of user_input into a single string
        user_input = " ".join(args.user_input)
        answer = temi_interface.handle_assitant(user_input)
        print(answer)
    elif args.command == "reddit":
        user_input = " ".join(args.user_input)
        answer = temi_interface.handle_reddit_news(user_input)
        print(answer)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
