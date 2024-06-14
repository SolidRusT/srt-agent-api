from srt_core.config import Config
from basic_chat import BasicChat

config = Config()

if config.debug:
    print("Debug mode is enabled")

chat_module = BasicChat(config)
# search_module = SearchModule(config)  # This will be used for future modules

while True:
    user_input = input(">")
    if user_input == "exit":
        break
    elif user_input.startswith("search:"):
        print("Search functionality is currently disabled.")
        # query = user_input[len("search:"):].strip()
        # results = search_module.search(query)  # Future use
        # print(f"Search Results: {results}")
    else:
        response = chat_module.chat(user_input)
        print(f"Agent: {response}")
