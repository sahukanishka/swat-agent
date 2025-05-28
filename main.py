import typer
from rich.console import Console
from rich.prompt import Prompt
from ai_agent import CommandAI
from config import OPENAI_API_KEY

app = typer.Typer()
console = Console()


def check_api_key():
    """Check if OpenAI API key is set."""
    if not OPENAI_API_KEY:
        console.print(
            "[red]Error: OPENAI_API_KEY not found in environment variables[/red]"
        )
        console.print("Please set your OpenAI API key in the .env file")
        raise typer.Exit(1)


@app.command()
def execute(
    command: str = typer.Argument(None, help="The natural language command to execute")
):
    """Execute a natural language command."""
    check_api_key()

    if not command:
        command = Prompt.ask("Enter your command")

    console.print(f"\n[bold blue]Processing command:[/bold blue] {command}\n")

    try:
        ai = CommandAI()
        result = ai.process_command(command)

        if result["success"]:
            console.print("\n[green]Command executed successfully![/green]")
        else:
            console.print("\n[red]Command execution failed![/red]")

    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


@app.command()
def history():
    """Show command execution history."""
    check_api_key()

    try:
        ai = CommandAI()
        history = ai.get_command_history()

        if not history:
            console.print("[yellow]No command history found[/yellow]")
            return

        console.print("\n[bold blue]Command History:[/bold blue]\n")
        for entry in history:
            console.print(f"[bold]Command:[/bold] {entry['command']}")
            console.print(f"[bold]Status:[/bold] {entry['status']}")
            console.print(f"[bold]Timestamp:[/bold] {entry['timestamp']}")
            if entry["status"] == "success":
                console.print(f"[bold]Output:[/bold]\n{entry['output']}")
            else:
                console.print(f"[bold]Error:[/bold]\n{entry['error']}")
            console.print("---")

    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
