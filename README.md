# SWAT CMD AI: Swift and Safe Command Execution Agent

A lightning-fast AI-powered command execution agent that understands natural language queries and executes terminal commands safely across different operating systems (macOS, Windows, and Ubuntu). SWAT (Swift and Safe) CMD AI is designed to be your intelligent command-line companion that executes tasks quickly while maintaining security.

## Features

- ⚡ Lightning-fast command execution
- 🛡️ Safe and validated command processing
- 🤖 Natural language command interpretation
- 🔄 Cross-platform command execution
- 🎯 Multi-agent orchestration using CrewAI
- 🧠 Support for multiple LLM backends (OpenAI, Gemini)
- 📝 Command history tracking
- 💻 Rich terminal interface
- 🚀 Simple `swat` command for instant access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/swat-cmd-ai.git
cd swat-cmd-ai
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

The fastest way to execute commands is through the `swat` command:

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

# System operations
swat "show me the current directory and list all files"
swat "check disk space usage"
swat "show running processes"
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

- 🛡️ Command validation before execution
- 🔒 Operating system-specific command adaptation
- 👮 Permission checks
- 📝 Command history logging
- ⚠️ Dangerous command prevention
- 🔍 Command context validation

## Why SWAT CMD AI?

- **Swift**: Executes commands quickly and efficiently
- **Safe**: Validates and secures all command execution
- **Smart**: Understands natural language and context
- **Simple**: Easy to use with the `swat` command
- **Secure**: Prevents dangerous operations
- **System-aware**: Adapts to your operating system

## License

MIT License 