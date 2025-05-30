import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Project paths
BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / "logs"
HISTORY_FILE = BASE_DIR / "command_history.json"

# Create necessary directories
LOGS_DIR.mkdir(exist_ok=True)

# LLM Configuration
DEFAULT_MODEL = "gpt-4-turbo-preview"  # or "gemini-pro"
TEMPERATURE = 0.7

# Command execution settings
MAX_COMMAND_LENGTH = 1000
ALLOWED_COMMANDS = {
    # Unix/Linux/macOS commands
    "ls",
    "dir",
    "cd",
    "mkdir",
    "rm",
    "cp",
    "mv",
    "touch",
    "cat",
    "echo",
    "grep",
    "find",
    "chmod",
    "chown",
    # Windows-specific commands
    "rmdir",
    "del",
    "copy",
    "move",
    "type",
    "echo",
    "dir",
    "cd",
    "mkdir",
    "rd",
    "copy",
    "xcopy",
    # Common commands
    "pwd",
    "clear",
    "cls",
    "whoami",
    "date",
    "time",
    # Process management commands
    "lsof",
    "kill",
    "ps",
    "top",
    "xargs",
    "pkill",
    "killall",
    "netstat",
    "taskkill",
    "tasklist",
    "netstat",
    "taskkill",
    "tasklist",
    "netstat",
    "taskkill",
    "tasklist",
    "netstat",
    "ping",
    "traceroute",
    "dig",
    "nslookup",
    "whois",
    "curl",
    "wget",
}

# Platform-specific settings
PLATFORM_COMMANDS = {
    "darwin": {  # macOS
        "list_dir": "ls -la",
        "create_dir": "mkdir",
        "remove": "rm -rf",
        "find_process": "lsof -i",
        "kill_process": "kill -9",
    },
    "win32": {  # Windows
        "list_dir": "dir",
        "create_dir": "mkdir",
        "remove": "rmdir /s /q",
        "find_process": "netstat -ano | findstr",
        "kill_process": "taskkill /F /PID",
    },
    "linux": {  # Ubuntu/Linux
        "list_dir": "ls -la",
        "create_dir": "mkdir",
        "remove": "rm -rf",
        "find_process": "lsof -i",
        "kill_process": "kill -9",
    },
}
