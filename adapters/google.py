from .openai_compatible import OpenAICompatibleAdapter
import os, time
from .base import ModelAdapter, ModelResponse
class GoogleAdapter(ModelAdapter):
    def generate(self, system_prompt, user_prompt, config):
        import google.generativeai as genai
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"]); start=time.perf_counter()
        model=genai.GenerativeModel(self.model_id, system_instruction=system_prompt)
        r=model.generate_content(user_prompt, generation_config={"temperature":config.get("temperature",0),"top_p":config.get("top_p",1.0),"max_output_tokens":config.get("max_output_tokens",500),"response_mime_type":"application/json"})
        return ModelResponse(r.text, model_id=self.model_id, provider=self.provider, latency_ms=(time.perf_counter()-start)*1000)
