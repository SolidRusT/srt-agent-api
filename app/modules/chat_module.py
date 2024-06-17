from app.modules.base_module import BaseModule

class ChatModule(BaseModule):
    def __init__(self, config, logger):
        required_modules = ["llama_cpp_agent"]
        super().__init__(config, logger, required_modules)

        if self.dependencies_available:
            self.provider = self._initialize_provider()
            self.agent = self._initialize_agent("You are a helpful assistant.")
        else:
            self.logger.info("Chat module dependencies are not installed. Disabling functionality.")

    def chat(self, message):
        if not self.dependencies_available:
            return "Chat functionality is disabled due to missing dependencies."
        try:
            response = self.agent.get_chat_response(message)
            return response
        except Exception as e:
            self.logger.error(f"Error processing chat request: {e}")
            return f"Error: {e}"

# Example usage
if __name__ == "__main__":
    from srt_core.config import Config
    from srt_core.utils.logger import Logger

    config = Config()
    logger = Logger()
    chat_module = ChatModule(config, logger)

    while True:
        user_input = input(">")
        if user_input == "exit":
            break
        response = chat_module.chat(user_input)
        print(f"Agent: {response}")
