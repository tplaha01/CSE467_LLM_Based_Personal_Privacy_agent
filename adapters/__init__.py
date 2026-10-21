from .base import ModelAdapter, ModelResponse
from .openai_compatible import OpenAICompatibleAdapter
from .openai import OpenAIAdapter
from .anthropic import AnthropicAdapter
from .google import GoogleAdapter
from .local_hf import LocalHFAdapter

def create_adapter(provider, model):
    classes={"openai_compatible":OpenAICompatibleAdapter,"openai":OpenAIAdapter,"anthropic":AnthropicAdapter,"google":GoogleAdapter,"local_hf":LocalHFAdapter}
    if provider not in classes: raise ValueError(f"unsupported provider: {provider}")
    return classes[provider](model, provider)
