from dataclasses import dataclass, field
from typing import Any
@dataclass
class ModelResponse:
    raw_text: str
    parsed_output: Any = None
    model_id: str = ""
    provider: str = ""
    input_tokens: int|None = None
    output_tokens: int|None = None
    latency_ms: float|None = None
    finish_reason: str|None = None
    request_metadata: dict = field(default_factory=dict)
@dataclass
class ModelAdapter:
    model_id: str
    provider: str
    def generate(self, system_prompt, user_prompt, config): raise NotImplementedError
