import os

HOST = os.environ.get("BSS_HOST", "127.0.0.1")
PORT = int(os.environ.get("BSS_PORT", "8060"))
CONTEXT_PATH = os.environ.get("BSS_CONTEXT_PATH", "/telecom-tmf-bss")

# How long a sign-in lasts.
SESSION_HOURS = int(os.environ.get("BSS_SESSION_HOURS", "24"))
