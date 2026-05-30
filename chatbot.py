import ollama
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)
ai_config = config.get("ai", {})
enabled = ai_config.get("enable", False)
model = None
system_prompt = ""
if enabled:
    model = ai_config.get("model")
    if model is None:
        raise ValueError("config.toml [ai] missing 'model'")
    system_prompt = ai_config.get("system_prompt", "")

messages = [
    {
        "role": "system",
        "content": system_prompt,
    }
] if system_prompt else []


def generate(msg):
    print("chating")
    if not enabled:
        return ""
    global messages
    messages.append({"role": "user", "content": msg})
    response = ollama.chat(model=model, messages=messages, think=False)
    text = response["message"]["content"]
    messages.append({"role": "assistant", "content": text})
    if messages[0]["role"] == "system":
        if len(messages) > 61:
            messages = [messages[0]] + messages[-6:]
    else:
        if len(messages) > 60:
            messages = messages[-6:]
    return text


if __name__ == "__main__":
    while True:
        print(generate(input(">")))
