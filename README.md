[English](README.md) | [简体中文](README_zh.md)

# OpenTTD LLM Chatbot

A Python script that runs an OpenTTD server and connects it to an LLM (via Ollama) for AI-powered chat responses.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install ollama
   ```

2. **Configure `config.toml`** (see Configuration section below)

3. **Run the server:**
   ```bash
   # With a save file
   python main.py <save_file_path>

   # With default save (no save file)
   python main.py
   ```

4. **Send commands:** Type commands directly in the terminal to send to OpenTTD console.

## Configuration

Edit `config.toml`:

```toml
[server]
log_file = "openttd_server.log"  # Path to log file (required)

[ai]
enable = true                 # Enable AI chat (required)
ignore_client = "ChatBotAI"   # Client name to ignore (optional, default: "")
model = "OTTD-Chatbot"        # Ollama model name (required when enable=true)
system_prompt = ""            # System prompt for the AI (optional, default: "")
```

### Options

| Section | Key | Required | Default | Description |
|---------|-----|----------|---------|-------------|
| server | log_file | Yes | - | Path to the log file |
| ai | enable | Yes | false | Enable AI chat functionality |
| ai | ignore_client | No | "" | Client name to ignore in chat |
| ai | model | Yes* | - | Ollama model name (*required when enable_ai=true) |
| ai | system_prompt | No | "" | System prompt for the AI |

