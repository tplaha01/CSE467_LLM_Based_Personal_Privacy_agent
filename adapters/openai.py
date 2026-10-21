from .openai_compatible import OpenAICompatibleAdapter
import os, time
from .base import ModelAdapter, ModelResponse
class OpenAIAdapter(ModelAdapter):
    def generate(self, system_prompt, user_prompt, config):
        from openai import OpenAI
        client=OpenAI(api_key=os.environ["OPENAI_API_KEY"]); start=time.perf_counter()
        r=client.chat.completions.create(model=self.model_id, messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}], response_format={"type":"json_object"}, temperature=config.get("temperature",0), top_p=config.get("top_p",1.0), max_tokens=config.get("max_output_tokens",500))
        c=r.choices[0]; u=getattr(r,"usage",None)
        return ModelResponse(c.message.content or "", model_id=self.model_id, provider=self.provider, input_tokens=getattr(u,"prompt_tokens",None), output_tokens=getattr(u,"completion_tokens",None), latency_ms=(time.perf_counter()-start)*1000, finish_reason=c.finish_reason)
