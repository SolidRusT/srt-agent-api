import json
from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from llama_cpp_agent import LlamaCppAgent, MessagesFormatterType
from llama_cpp_agent.chat_history import BasicChatHistory
from app.modules.base_module import BaseModule

class ReflectionState(Enum):
    approved = "approved"
    rejected = "rejected"

class Reflection(BaseModel):
    analysis: str = Field(..., description="Analysis of the latest response")
    critique: str = Field(..., description="Critique of the latest response")
    things_to_improve: List[str] = Field(default_factory=list, description="List of things to improve")
    response_state: ReflectionState = Field(..., description="The decision if this response is approved or rejected")

class AgenticReflectionModule(BaseModule):
    def __init__(self, config, logger):
        super().__init__(config, logger, ["llama_cpp_agent"])
        if self.dependencies_available:
            self.provider = self._initialize_provider(config.default_llm_settings)
            self.chat_history = BasicChatHistory(k=35)

            self.generator_agent = LlamaCppAgent(
                self.provider,
                debug_output=True,
                system_prompt="You are a misinformed AI agent.",
                predefined_messages_formatter_type=MessagesFormatterType.MISTRAL,
                chat_history=self.chat_history
            )

            self.reflection_agent = LlamaCppAgent(
                self.provider,
                system_prompt="Your task is to analyze, provide feedback and critique on an AI agent's latest response to a user in an ongoing conversation. You then decide if the latest response is approved or rejected.",
                debug_output=True,
                predefined_messages_formatter_type=MessagesFormatterType.MISTRAL
            )

    def get_reflective_response(self, input_message: str):
        approved = False
        while not approved:
            self.generator_agent.get_chat_response(input_message)
            messages = self.generator_agent.chat_history.get_chat_messages()
            ctx = ""
            for message in messages:
                ctx += f"{json.dumps(message, indent=2)}\n\n"

            reflection_response = self.reflection_agent.get_chat_response(ctx)
            reflection_data = json.loads(reflection_response)

            if reflection_data["response_state"] == ReflectionState.approved.value:
                approved = True

        return self.generator_agent.chat_history.get_latest_message().content

# Example usage
if __name__ == "__main__":
    from srt_core.config import Config
    from srt_core.utils.logger import Logger

    config = Config()
    logger = Logger()
    agentic_reflection_module = AgenticReflectionModule(config, logger)
    print(agentic_reflection_module.get_reflective_response("Write a summary about the independence war of America against England."))
