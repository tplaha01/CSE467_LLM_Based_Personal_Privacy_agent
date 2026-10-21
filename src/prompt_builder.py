from pathlib import Path
def build_prompt(statement, prompt_path="prompts/harm_detection_v1.txt"):
    return Path(prompt_path).read_text(encoding="utf-8").replace("<<<STATEMENT>>>", statement)
