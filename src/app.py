from srt_core.config import Config
from chat_module import ChatModule
from search_module import SearchModule

config = Config()

if config.debug:
    print("Debug mode is enabled")

chat_module = ChatModule(config)
search_module = SearchModule(config)

while True:
    user_input = input(">")
    if user_input == "exit":
        break
    elif user_input.startswith("search:"):
        query = user_input[len("search:"):].strip()
        results = search_module.search(query)
        print(f"Search Results: {results}")
    else:
        response = chat_module.chat(user_input)
        print(f"Agent: {response}")
