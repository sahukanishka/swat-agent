from crewai import Agent, Task, Crew, Process
from typing import List, Dict
import platform
import os
from config import DEFAULT_MODEL, TEMPERATURE, OPENAI_API_KEY
from command_executor import CommandExecutor, MultiCommandExecutor
from rich.console import Console

console = Console()


class CommandAI:
    def __init__(self):
        self.command_executor = MultiCommandExecutor()
        self.platform = platform.system().lower()
        self.current_dir = os.getcwd()

        # Initialize agents
        self.command_interpreter = Agent(
            role="Command Interpreter",
            goal="Interpret natural language commands into executable terminal commands",
            backstory="""You are an expert at understanding natural language and converting it into 
            precise terminal commands. You understand the nuances of different operating systems 
            and can adapt commands accordingly. You can break down complex tasks into multiple sequential commands.
            
            For process management:
            - To find a process on a port: lsof -i :PORT
            - To kill a process: kill -9 PID
            - To find and kill in one command: lsof -ti :PORT | xargs kill -9
            
            For file operations:
            - To find files: find . -name "filename"
            - To check file contents: cat filename
            - To append to files: echo "content" >> filename
            
            Always use the most efficient and safe command combination.
            Always consider the current working directory context.""",
            verbose=False,
            allow_delegation=False,
            llm_model=DEFAULT_MODEL,
            temperature=TEMPERATURE,
        )

        self.command_validator = Agent(
            role="Command Validator",
            goal="Validate and ensure the safety of terminal commands",
            backstory="""You are a security expert who validates terminal commands for safety 
            and potential risks. You ensure that commands are safe to execute and won't cause 
            harm to the system. You can validate multiple sequential commands.
            
            For process management:
            - Always verify the process exists before killing
            - Use appropriate signal numbers (9 for force kill)
            - Combine find and kill operations when safe to do so
            
            For file operations:
            - Verify file existence before operations
            - Use safe file manipulation commands
            - Handle file permissions appropriately
            
            Always ensure commands respect the current working directory context.""",
            verbose=False,
            allow_delegation=False,
            llm_model=DEFAULT_MODEL,
            temperature=TEMPERATURE,
        )

    def process_command(self, natural_language_command: str) -> Dict:
        """Process a natural language command and execute it safely."""
        try:
            # Create tasks
            interpretation_task = Task(
                description=f"""Convert the following natural language command into one or more terminal commands for {self.platform} system.
                Command: {natural_language_command}
                Current Working Directory: {self.current_dir}
                
                IMPORTANT: 
                - Return a list of terminal commands separated by newlines, with no explanations or additional text.
                - Each command should be on a new line.
                - Commands should be executed in the current working directory: {self.current_dir}
                - Do not use absolute paths unless specifically requested
                
                For process management:
                - To find and kill a process on port X: lsof -ti :X | xargs kill -9
                - To find a process: lsof -i :X
                - To kill a process: kill -9 PID
                
                For file operations:
                - To find files: find . -name "filename"
                - To check file contents: cat filename
                - To append to files: echo "content" >> filename
                
                Consider:
                1. The current operating system ({self.platform})
                2. The most efficient way to achieve the goal
                3. Safety and best practices
                4. Current working directory context
                5. Command dependencies and sequence""",
                agent=self.command_interpreter,
                expected_output="A list of terminal commands, one per line, without any explanation or additional text.",
            )

            validation_task = Task(
                description=f"""Validate the interpreted commands for safety and correctness.
                Current Working Directory: {self.current_dir}
                
                IMPORTANT: Return the validated commands, one per line, with no explanations or additional text.
                
                For process management:
                - Ensure the commands include proper error handling
                - Verify the process exists before killing
                - Use appropriate signal numbers
                
                For file operations:
                - Verify file existence before operations
                - Use safe file manipulation commands
                - Handle file permissions appropriately
                
                Check for:
                1. Potentially dangerous operations
                2. Proper syntax
                3. Platform compatibility
                4. Working directory context
                5. Command sequence validity
                
                If the commands are safe, return them as is. If not, return safer alternative commands.""",
                agent=self.command_validator,
                expected_output="A list of validated terminal commands, one per line, without any explanation or additional text.",
                context=[interpretation_task],
            )

            # Create and run the crew
            crew = Crew(
                agents=[self.command_interpreter, self.command_validator],
                tasks=[interpretation_task, validation_task],
                verbose=False,
                process=Process.sequential,
            )

            result = crew.kickoff()

            # Extract the commands from the CrewOutput and clean them
            commands = str(result).strip().split("\n")
            commands = [cmd.strip().strip("\"'") for cmd in commands if cmd.strip()]

            if not commands:
                error_msg = "No valid commands were generated"
                console.print(f"[red]{error_msg}[/red]")
                return {
                    "original_command": natural_language_command,
                    "error": error_msg,
                    "working_directory": self.current_dir,
                }

            # Execute the commands sequentially
            results = self.command_executor.execute_sequential_commands(commands)

            # Display results for each command
            for result in results:
                self.command_executor.display_result(
                    result["success"], result["output"]
                )

            return {
                "original_command": natural_language_command,
                "interpreted_commands": commands,
                "results": results,
                "working_directory": self.current_dir,
            }

        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            console.print(f"[red]{error_msg}[/red]")
            return {
                "original_command": natural_language_command,
                "error": error_msg,
                "working_directory": self.current_dir,
            }

    def get_command_history(self) -> List[Dict]:
        """Get the history of executed commands."""
        return self.command_executor.get_command_history()
