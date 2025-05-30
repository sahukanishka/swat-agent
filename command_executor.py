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
        try:
            style = "green" if success else "red"
            # Ensure message is a string and not None
            message = str(message) if message is not None else ""
            console.print(
                Panel(
                    f"Working Directory: {self.original_cwd}\n\n{message}",
                    title="Command Result",
                    style=style,
                )
            )
        except Exception as e:
            console.print(f"[red]Error displaying result: {str(e)}[/red]")
            # Fallback display
            console.print(
                f"[{'green' if success else 'red'}]Command {'succeeded' if success else 'failed'}[/{'green' if success else 'red'}]"
            )
            if message:
                console.print(f"Output: {message}")

    def get_command_history(self) -> List[Dict]:
        """Get command execution history."""
        return self.command_history


class MultiCommandExecutor(CommandExecutor):
    def __init__(self):
        super().__init__()
        self.command_results = []

    def execute_sequential_commands(self, commands: List[str]) -> List[Dict]:
        """
        Execute a list of commands sequentially, where each command can depend on the result of previous commands.

        Args:
            commands: List of commands to execute in sequence

        Returns:
            List of dictionaries containing the results of each command execution
        """
        results = []

        for command in commands:
            try:
                # Validate command first
                is_valid, message = self.validate_command(command)
                if not is_valid:
                    result = {
                        "command": command,
                        "success": False,
                        "output": f"Invalid command: {message}",
                        "timestamp": datetime.now().isoformat(),
                    }
                    results.append(result)
                    console.print(f"[red]Invalid command: {command}[/red]")
                    console.print(f"[red]Error: {message}[/red]")
                    break

                # Execute the command
                success, output = self.execute_command(command)
                result = {
                    "command": command,
                    "success": success,
                    "output": output,
                    "timestamp": datetime.now().isoformat(),
                }
                results.append(result)

                # If a command fails, we might want to stop the sequence
                if not success:
                    console.print(f"[red]Command failed: {command}[/red]")
                    console.print(f"[red]Error: {output}[/red]")
                    break

            except Exception as e:
                error_result = {
                    "command": command,
                    "success": False,
                    "output": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
                results.append(error_result)
                console.print(f"[red]Error executing command: {command}[/red]")
                console.print(f"[red]Error details: {str(e)}[/red]")
                break

        self.command_results = results
        return results

    def get_last_result(self) -> Optional[Dict]:
        """Get the result of the last executed command."""
        return self.command_results[-1] if self.command_results else None

    def get_all_results(self) -> List[Dict]:
        """Get all command execution results."""
        return self.command_results

    def clear_results(self):
        """Clear the command results history."""
        self.command_results = []

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
