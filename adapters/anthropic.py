from .openai_compatible import OpenAICompatibleAdapter
import os, time
from .base import ModelAdapter, ModelResponse
class AnthropicAdapter(ModelAdapter):
    def generate(self, system_prompt, user_prompt, config):
        import anthropic
        client=anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"]); start=time.perf_counter()
        r=client.messages.create(model=self.model_id, system=system_prompt, messages=[{"role":"user","content":user_prompt}], max_tokens=config.get("max_output_tokens",500), temperature=config.get("temperature",0), top_p=config.get("top_p",1.0))
        text="".join(getattr(x,"text","") for x in r.content)
        return ModelResponse(text, model_id=self.model_id, provider=self.provider, input_tokens=getattr(r.usage,"input_tokens",None), output_tokens=getattr(r.usage,"output_tokens",None), latency_ms=(time.perf_counter()-start)*1000, finish_reason=getattr(r,"stop_reason",None))
