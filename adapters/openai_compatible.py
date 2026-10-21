import os, time
from .base import ModelAdapter, ModelResponse
class OpenAICompatibleAdapter(ModelAdapter):
    def generate(self, system_prompt, user_prompt, config):
        try:
            from openai import OpenAI
        except ImportError as e: raise RuntimeError("install openai") from e
        key=os.getenv("TOKENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
        client=OpenAI(api_key=key, base_url=os.getenv("OPENAI_COMPATIBLE_BASE_URL"))
        requested={k:config[k] for k in ("temperature","top_p","max_output_tokens") if k in config}
        start=time.perf_counter(); r=client.chat.completions.create(model=self.model_id, messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}], response_format={"type":"json_object"}, **requested)
        choice=r.choices[0]; usage=getattr(r,"usage",None)
        return ModelResponse(choice.message.content or "", model_id=self.model_id, provider=self.provider, input_tokens=getattr(usage,"prompt_tokens",None), output_tokens=getattr(usage,"completion_tokens",None), latency_ms=(time.perf_counter()-start)*1000, finish_reason=choice.finish_reason, request_metadata={"requested":requested,"accepted":requested})
