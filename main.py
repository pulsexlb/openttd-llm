import subprocess
import datetime
import sys
import select
import os
import re
import tomllib
import chatbot

CHAT_PATTERN = re.compile(r"\[All\]\s+([^:]+):\s*(.*)$")


def load_config(config_path="config.toml"):
    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    log_file = config.get("server", {}).get("log_file")
    if log_file is None:
        raise ValueError("config.toml [server] missing 'log_file'")
    
    ai_config = config.get("ai", {})
    enable_ai = ai_config.get("enable", False)
    
    ignore_client = ""
    model = None
    
    if enable_ai:
        ignore_client = ai_config.get("ignore_client", "")
        model = ai_config.get("model")
        if model is None:
            raise ValueError("config.toml [ai] missing 'model'")

    return log_file, ignore_client, model, enable_ai


def start_server(save_path):
    if save_path:
        return subprocess.Popen(
            ["openttd", "-D", "-g", save_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            text=False,
        )
    else:
        return subprocess.Popen(
            ["openttd", "-D"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            text=False,
        )


def main(initial_save_path):
    log_file, ignore_client, model, enable_ai = load_config()
    chatbot.enabled = enable_ai
    current_path = initial_save_path

    print(f"[LOADER][{datetime.datetime.now()}] Starting server with: {current_path or 'default'}")

    log_fp = open(log_file, "a")
    proc = start_server(current_path)

    while True:
        ready, _, _ = select.select([proc.stdout, sys.stdin], [], [], 1.0)

        if sys.stdin in ready:
            user_input = sys.stdin.readline()
            if user_input:
                proc.stdin.write(user_input.encode())
                proc.stdin.flush()

        if proc.stdout in ready:
            line = proc.stdout.readline()
            if not line:
                if proc.poll() is not None:
                    print("[LOADER]Process exited unexpectedly")
                    break
                continue

            text = line.decode("utf-8", errors="replace")
            sys.stdout.write(text)
            sys.stdout.flush()
            log_fp.write(text)
            log_fp.flush()

            match_msg = CHAT_PATTERN.search(text)
            if match_msg:
                player_name, message = match_msg.groups()
                if player_name != ignore_client and enable_ai:
                    print(player_name + " said " + message)
                    resp = chatbot.generate(message)
                    for res_line in resp.split("\n"):
                        proc.stdin.write(f'say "{res_line}"\n'.encode())
                    proc.stdin.flush()


if __name__ == "__main__":
    save_path = sys.argv[1] if len(sys.argv) > 1 else None
    main(save_path)
