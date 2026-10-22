import json, os, time
from urllib.request import Request, urlopen
from pathlib import Path
from .base import ModelAdapter, ModelResponse
class OpenAICompatibleAdapter(ModelAdapter):
    def generate(self, system_prompt, user_prompt, config):
        base=(os.getenv("OPENAI_COMPATIBLE_BASE_URL") or "").rstrip("/")
        if base.endswith(":11434/v1"):
            schema=json.loads(Path("schemas/prediction.schema.json").read_text(encoding="utf-8"))
            payload={"model":self.model_id,"messages":[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}],"format":schema,"stream":False,"options":{"temperature":config.get("temperature",0),"top_p":config.get("top_p",1.0),"num_predict":config.get("max_output_tokens",500)}}
            start=time.perf_counter(); req=Request("http://127.0.0.1:11434/api/chat",data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"},method="POST")
            with urlopen(req,timeout=config.get("timeout_seconds",60)) as response:
                body=json.loads(response.read().decode("utf-8"))
            return ModelResponse(body.get("message",{}).get("content","") , model_id=self.model_id, provider=self.provider, input_tokens=body.get("prompt_eval_count"), output_tokens=body.get("eval_count"), latency_ms=(time.perf_counter()-start)*1000, finish_reason="stop", request_metadata={"native_ollama":True,"structured_output":True})
        try:
            from openai import OpenAI
        except ImportError as e: raise RuntimeError("install openai") from e
        key=os.getenv("TOKENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
        client=OpenAI(api_key=key, base_url=os.getenv("OPENAI_COMPATIBLE_BASE_URL"))
        requested={k:config[k] for k in ("temperature","top_p") if k in config}
        if "max_output_tokens" in config:
            requested["max_tokens"] = config["max_output_tokens"]
        kwargs={"model":self.model_id,"messages":[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}],**requested}
        # Ollama's OpenAI-compatible JSON mode can truncate Qwen 4B responses
        # after the first object. The prompt plus local schema validation still
        # enforce JSON, while omitting this flag preserves the full response.
        if base.endswith(":11434/v1"):
            schema_path=Path("schemas/prediction.schema.json")
            if schema_path.exists():
                kwargs["extra_body"]={"format":json.loads(schema_path.read_text(encoding="utf-8"))}
        else:
            kwargs["response_format"]={"type":"json_object"}
        start=time.perf_counter(); r=client.chat.completions.create(**kwargs)
        choice=r.choices[0]; usage=getattr(r,"usage",None)
        return ModelResponse(choice.message.content or "", model_id=self.model_id, provider=self.provider, input_tokens=getattr(usage,"prompt_tokens",None), output_tokens=getattr(usage,"completion_tokens",None), latency_ms=(time.perf_counter()-start)*1000, finish_reason=choice.finish_reason, request_metadata={"requested":requested,"accepted":requested})
