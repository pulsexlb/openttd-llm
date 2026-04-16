import subprocess
import datetime
import sys
import select
import os
import re
import chatbot

LOG_FILE = "openttd_server.log"
SAVE_DIR = os.path.expanduser("~/.local/share/openttd/save/")
CHAT_PATTERN = re.compile(r"\[All\]\s+([^:]+):\s*(.*)$")


def get_save_name():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def start_server(save_path):
    return subprocess.Popen(
        ["openttd", "-D", "-g", save_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        text=False,
    )


def main(initial_save_path):
    current_path = initial_save_path

    print(f"[LOADER][{datetime.datetime.now()}] Starting server with: {current_path}")

    log_fp = open(LOG_FILE, "a")
    proc = start_server(current_path)

    just_saying = False

    while True:
        ready, _, _ = select.select([proc.stdout], [], [], 1.0)

        if ready:

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

            if match_msg and not just_saying:
                player_name, message = match_msg.groups()
                print(player_name + " said " + message)
                resp = chatbot.generate(message)
                for res_line in resp.split("\n"):
                    proc.stdin.write(f"say \"{res_line}\"\n".encode())
                proc.stdin.flush()
                just_saying = True
            elif just_saying:
                just_saying = False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <save_file_path>")
        sys.exit(1)
    main(sys.argv[1])
