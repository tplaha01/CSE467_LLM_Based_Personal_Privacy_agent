from .openai_compatible import OpenAICompatibleAdapter
import time
from .base import ModelAdapter, ModelResponse
class LocalHFAdapter(ModelAdapter):
    def generate(self, system_prompt, user_prompt, config):
        from transformers import pipeline
        start=time.perf_counter(); pipe=pipeline("text-generation", model=self.model_id)
        prompt=system_prompt+"\n\n"+user_prompt; result=pipe(prompt, max_new_tokens=config.get("max_output_tokens",500), do_sample=False)
        text=result[0]["generated_text"][len(prompt):]
        return ModelResponse(text, model_id=self.model_id, provider=self.provider, latency_ms=(time.perf_counter()-start)*1000)
