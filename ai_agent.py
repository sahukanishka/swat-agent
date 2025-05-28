from crewai import Agent, Task, Crew, Process
from typing import List, Dict
import platform
import os
from config import DEFAULT_MODEL, TEMPERATURE, OPENAI_API_KEY
from command_executor import CommandExecutor


class CommandAI:
    def __init__(self):
        self.command_executor = CommandExecutor()
        self.platform = platform.system().lower()
        self.current_dir = os.getcwd()

        # Initialize agents
        self.command_interpreter = Agent(
            role="Command Interpreter",
            goal="Interpret natural language commands into executable terminal commands",
            backstory="""You are an expert at understanding natural language and converting it into 
            precise terminal commands. You understand the nuances of different operating systems 
            and can adapt commands accordingly. You ONLY return the command itself, with no explanations or additional text.
            
            For process management:
            - To find a process on a port: lsof -i :PORT
            - To kill a process: kill -9 PID
            - To find and kill in one command: lsof -ti :PORT | xargs kill -9
            
            Always use the most efficient and safe command combination.
            Always consider the current working directory context.""",
            verbose=True,
            allow_delegation=False,
            llm_model=DEFAULT_MODEL,
            temperature=TEMPERATURE,
        )

        self.command_validator = Agent(
            role="Command Validator",
            goal="Validate and ensure the safety of terminal commands",
            backstory="""You are a security expert who validates terminal commands for safety 
            and potential risks. You ensure that commands are safe to execute and won't cause 
            harm to the system. You ONLY return the validated command, with no explanations or additional text.
            
            For process management:
            - Always verify the process exists before killing
            - Use appropriate signal numbers (9 for force kill)
            - Combine find and kill operations when safe to do so
            
            Always ensure commands respect the current working directory context.""",
            verbose=True,
            allow_delegation=False,
            llm_model=DEFAULT_MODEL,
            temperature=TEMPERATURE,
        )

    def process_command(self, natural_language_command: str) -> Dict:
        """Process a natural language command and execute it safely."""

        # Create tasks
        interpretation_task = Task(
            description=f"""Convert the following natural language command into a terminal command for {self.platform} system.
            Command: {natural_language_command}
            Current Working Directory: {self.current_dir}
            
            IMPORTANT: 
            - Return ONLY the terminal command itself, with no explanations or additional text.
            - Commands should be executed in the current working directory: {self.current_dir}
            - Do not use absolute paths unless specifically requested
            
            For process management:
            - To find and kill a process on port X: lsof -ti :X | xargs kill -9
            - To find a process: lsof -i :X
            - To kill a process: kill -9 PID
            
            Consider:
            1. The current operating system ({self.platform})
            2. The most efficient way to achieve the goal
            3. Safety and best practices
            4. Current working directory context""",
            agent=self.command_interpreter,
            expected_output="A single terminal command string without any explanation or additional text.",
        )

        validation_task = Task(
            description=f"""Validate the interpreted command for safety and correctness.
            Current Working Directory: {self.current_dir}
            
            IMPORTANT: Return ONLY the validated command itself, with no explanations or additional text.
            
            For process management:
            - Ensure the command includes proper error handling
            - Verify the process exists before killing
            - Use appropriate signal numbers
            
            Check for:
            1. Potentially dangerous operations
            2. Proper syntax
            3. Platform compatibility
            4. Working directory context
            
            If the command is safe, return it as is. If not, return a safer alternative command.""",
            agent=self.command_validator,
            expected_output="A single validated terminal command string without any explanation or additional text.",
            context=[interpretation_task],
        )

        # Create and run the crew
        crew = Crew(
            agents=[self.command_interpreter, self.command_validator],
            tasks=[interpretation_task, validation_task],
            verbose=True,
            process=Process.sequential,
        )

        result = crew.kickoff()

        # Extract the final command from the CrewOutput and clean it
        final_command = str(result).strip()
        # Remove any quotes if present
        final_command = final_command.strip("\"'")

        # Execute the validated command
        success, output = self.command_executor.execute_command(final_command)
        self.command_executor.display_result(success, output)

        return {
            "original_command": natural_language_command,
            "interpreted_command": final_command,
            "success": success,
            "output": output,
            "working_directory": self.current_dir,
        }

    def get_command_history(self) -> List[Dict]:
        """Get the history of executed commands."""
        return self.command_executor.get_command_history()
