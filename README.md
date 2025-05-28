# CMD-AI: Natural Language Command Execution Agent

A powerful AI-powered command execution agent that understands natural language queries and executes terminal commands across different operating systems (macOS, Windows, and Ubuntu).

## Features

- Natural language command interpretation
- Cross-platform command execution
- Multi-agent orchestration using CrewAI
- Support for multiple LLM backends (OpenAI, Gemini)
- Safe command execution with validation
- Rich terminal interface
- Simple `swat` command for easy access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cmd-ai.git
cd cmd-ai
```

2. Run the installation script:
```bash
chmod +x install.sh
./install.sh
```

3. Create a `.env` file and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

## Usage

### Using the `swat` command

The easiest way to use the agent is through the `swat` command:

```bash
swat "your natural language command"
```

Examples:
```bash
# Find and kill a process on port 8080
swat "find the port 8080 and kill it"

# Create a new directory and list its contents
swat "create a new directory called projects and list all files in it"

# Search for a file
swat "find all .py files in the current directory"
```

### Using the Python script directly

You can also use the Python script directly:

```bash
python main.py execute "your natural language command"
```

To view command history:
```bash
python main.py history
```

## Safety Features

- Command validation before execution
- Operating system-specific command adaptation
- Permission checks
- Command history logging

## License

MIT License 