import re
import ollama

model = "BigGe"

messages = [
    {
        "role": "system",
        "content": "你是大哥，你是openttd游戏qq群的群主。你曾多次承诺群友即将开openttd游戏服务器，但是多次食言，如今，你仍然承诺很快就会开服。你在私底下求助其他人(破产是你主要的求助对象)询问开服的技术要点，你尝试使用linux，但是你一点都不会使用。你时常问出一些十分幼稚的技术问题。现在，你需要继续欺骗群友，如果问你技术是否需要技术相关帮助，你会问一些很基础的技术问题。注意：你需要避免重复说同一句话，你可以输出多行内容",
    }
]


def generate(msg):
    global messages
    messages.append({"role": "user", "content": msg})
    response = ollama.chat(model=model, messages=messages)
    res_text = re.sub(
        r"<think>.*?</think>", "", response["message"]["content"], flags=re.DOTALL
    ).strip()
    messages.append({"role": "assistant", "content": res_text})
    if messages[0]["role"] == "system":
        # 有系统提示：保留 system + 最后 60 条
        if len(messages) > 61:
            messages = [messages[0]] + messages[-6:]
    else:
        # 无系统提示：只保留最后 60 条
        if len(messages) > 60:
            messages = messages[-6:]
    return res_text


if __name__ == "__main__":
    while True:
        print(generate(input(">")))

