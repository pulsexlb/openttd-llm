[English](README.md) | [简体中文](README_zh.md)

# OpenTTD LLM 聊天机器人

一个 Python 脚本，用于运行 OpenTTD 服务器并将其连接到 LLM（通过 Ollama）以实现 AI 聊天回复。

## 快速开始

1. **安装依赖：**
   ```bash
   pip install ollama
   ```

2. **配置 `config.toml`**（参见配置部分）

3. **运行服务器：**
   ```bash
   # 使用存档文件
   python main.py <存档文件路径>

   # 使用默认存档（无存档文件）
   python main.py
   ```

4. **发送命令：直接在终端中输入命令发送到 OpenTTD 控制台。**

## 配置

编辑 `config.toml`：

```toml
[server]
log_file = "openttd_server.log"  # 日志文件路径（必填）

[ai]
enable = true                 # 启用 AI 聊天（必填）
ignore_client = "ChatBotAI"   # 要忽略的客户端名称（可选，默认: ""）
model = "OTTD-Chatbot"        # Ollama 模型名称（启用 AI 时必填）
system_prompt = ""            # AI 系统提示（可选，默认: ""）
```

### 选项说明

| 章节 | 键 | 必填 | 默认值 | 描述 |
|------|-----|------|--------|------|
| server | log_file | 是 | - | 日志文件路径 |
| ai | enable | 是 | false | 启用 AI 聊天功能 |
| ai | ignore_client | 否 | "" | 聊天中要忽略的客户端名称 |
| ai | model | 是* | - | Ollama 模型名称（启用 AI 时必填）|
| ai | system_prompt | 否 | "" | AI 系统提示 |
