import subprocess
import platform
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from rich.console import Console
from rich.panel import Panel
from config import PLATFORM_COMMANDS, ALLOWED_COMMANDS, HISTORY_FILE, MAX_COMMAND_LENGTH

console = Console()


class CommandExecutor:
    def __init__(self):
        self.platform = platform.system().lower()
        self.command_history: List[Dict] = []
        self._load_history()
        self.original_cwd = os.getcwd()  # Store the original working directory

    def _load_history(self):
        """Load command history from file."""
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r") as f:
                    self.command_history = json.load(f)
            except json.JSONDecodeError:
                self.command_history = []

    def _save_history(self):
        """Save command history to file."""
        with open(HISTORY_FILE, "w") as f:
            json.dump(self.command_history, f, indent=2)

    def validate_command(self, command: str) -> Tuple[bool, str]:
        """Validate if the command is safe to execute."""
        if len(command) > MAX_COMMAND_LENGTH:
            return False, "Command exceeds maximum length"

        # Basic command validation
        first_word = command.split()[0].lower()
        if first_word not in ALLOWED_COMMANDS:
            return False, f"Command '{first_word}' is not in the allowed commands list"

        # Add more validation rules here
        return True, "Command is valid"

    def execute_command(self, command: str) -> Tuple[bool, str]:
        """Execute a command and return the result."""
        # Validate command
        is_valid, message = self.validate_command(command)
        if not is_valid:
            return False, message

        try:
            # Execute command in the current working directory
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=True,
                cwd=self.original_cwd,  # Use the original working directory
            )

            # Log command execution
            self.command_history.append(
                {
                    "command": command,
                    "output": result.stdout,
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                    "working_directory": self.original_cwd,
                }
            )
            self._save_history()

            return True, result.stdout

        except subprocess.CalledProcessError as e:
            error_msg = f"Command failed with error: {e.stderr}"
            self.command_history.append(
                {
                    "command": command,
                    "error": error_msg,
                    "timestamp": datetime.now().isoformat(),
                    "status": "error",
                    "working_directory": self.original_cwd,
                }
            )
            self._save_history()
            return False, error_msg

    def get_platform_command(self, command_type: str) -> Optional[str]:
        """Get platform-specific command."""
        return PLATFORM_COMMANDS.get(self.platform, {}).get(command_type)

    def display_result(self, success: bool, message: str):
        """Display command execution result in a formatted way."""
        style = "green" if success else "red"
        console.print(
            Panel(
                f"Working Directory: {self.original_cwd}\n\n{message}",
                title="Command Result",
                style=style,
            )
        )

    def get_command_history(self) -> List[Dict]:
        """Get command execution history."""
        return self.command_history
