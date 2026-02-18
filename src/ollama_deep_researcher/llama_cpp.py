"""llama-cpp-server integration for the research assistant."""

import json
import logging
from typing import Any, List, Optional

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.tools import BaseTool
from pydantic import Field
import requests

logger = logging.getLogger(__name__)


class ChatLlamaCpp(BaseChatModel):
    """Chat model that uses llama-cpp-server's OpenAI-compatible API."""

    format: Optional[str] = Field(
        default=None, description="Format for the response (e.g., 'json')"
    )

    base_url: str = Field(
        default="http://127.0.0.1:8080/v1",
        description="Base URL for llama-cpp-server's OpenAI-compatible API",
    )
    model: str = Field(default="llama-3.2", description="Model name to use")
    temperature: float = Field(
        default=0.7, description="Temperature for sampling (0.0 - 2.0)"
    )
    top_p: float = Field(
        default=0.95, description="Nucleus sampling parameter (0.0 - 1.0)"
    )
    min_p: float = Field(
        default=0.05, description="Minimum probability threshold (0.0 - 0.5)"
    )
    api_key: str = Field(
        default="not-needed",
        description="API key (not actually used)",
    )

    @property
    def _llm_type(self) -> str:
        return "llama_cpp"

    def bind_tools(self, tools: List[BaseTool], **kwargs: Any) -> "ChatLlamaCpp":
        return self

    def _convert_message_to_dict(self, message: BaseMessage) -> dict:
        if isinstance(message, HumanMessage):
            return {"role": "user", "content": message.content}
        elif isinstance(message, SystemMessage):
            return {"role": "system", "content": message.content}
        elif isinstance(message, AIMessage):
            return {"role": "assistant", "content": message.content}
        else:
            return {"role": message.type, "content": message.content}

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        base_url = self.base_url.rstrip("/")
        api_url = f"{base_url}/chat/completions"

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [self._convert_message_to_dict(msg) for msg in messages],
            "temperature": self.temperature,
        }

        if self.top_p and self.top_p > 0:
            payload["top_p"] = self.top_p
        if self.min_p and self.min_p > 0:
            payload["min_p"] = self.min_p

        if self.format == "json":
            payload["response_format"] = {"type": "json_object"}

        if stop:
            payload["stop"] = stop

        try:
            response = requests.post(
                api_url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                },
                timeout=180,
            )

            if response.status_code != 200:
                raise Exception(f"API error {response.status_code}: {response.text}")

            result = response.json()

            if "choices" not in result or not result["choices"]:
                raise Exception(f"No choices in response: {result}")

            content = result["choices"][0]["message"]["content"]

            if self.format == "json":
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    json_text = content[json_start:json_end]
                    json.loads(json_text)
                    content = json_text

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

        generation = ChatGeneration(message=AIMessage(content=content))
        return ChatResult(generations=[generation])
