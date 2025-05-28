import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from ai_agent import CommandAI
from config import OPENAI_API_KEY

app = typer.Typer()
console = Console()


def check_api_key():
    """Check if OpenAI API key is set."""
    if not OPENAI_API_KEY:
        console.print(
            Panel(
                "[red]Error: OPENAI_API_KEY not found in environment variables[/red]\n"
                "Please set your OpenAI API key in the .env file",
                title="SWAT CMD AI Error",
                border_style="red",
            )
        )
        raise typer.Exit(1)


@app.command()
def execute(
    command: str = typer.Argument(None, help="The natural language command to execute")
):
    """Execute a natural language command."""
    check_api_key()

    if not command:
        command = Prompt.ask("Enter your command")

    console.print(
        Panel(
            f"[bold blue]Processing command:[/bold blue] {command}",
            title="SWAT CMD AI",
            border_style="blue",
        )
    )

    try:
        ai = CommandAI()
        result = ai.process_command(command)

        if result["success"]:
            console.print(
                Panel(
                    "\n[green]Command executed successfully![/green]",
                    title="SWAT CMD AI",
                    border_style="green",
                )
            )
        else:
            console.print(
                Panel(
                    "\n[red]Command execution failed![/red]",
                    title="SWAT CMD AI",
                    border_style="red",
                )
            )

    except Exception as e:
        console.print(
            Panel(
                f"\n[red]Error:[/red] {str(e)}",
                title="SWAT CMD AI Error",
                border_style="red",
            )
        )
        raise typer.Exit(1)


@app.command()
def history():
    """Show command execution history."""
    check_api_key()

    try:
        ai = CommandAI()
        history = ai.get_command_history()

        if not history:
            console.print(
                Panel(
                    "[yellow]No command history found[/yellow]",
                    title="SWAT CMD AI History",
                    border_style="yellow",
                )
            )
            return

        console.print(
            Panel(
                "\n[bold blue]Command History:[/bold blue]\n",
                title="SWAT CMD AI History",
                border_style="blue",
            )
        )
        for entry in history:
            console.print(f"[bold]Command:[/bold] {entry['command']}")
            console.print(f"[bold]Status:[/bold] {entry['status']}")
            console.print(f"[bold]Timestamp:[/bold] {entry['timestamp']}")
            console.print(
                f"[bold]Working Directory:[/bold] {entry.get('working_directory', 'N/A')}"
            )
            if entry["status"] == "success":
                console.print(f"[bold]Output:[/bold]\n{entry['output']}")
            else:
                console.print(f"[bold]Error:[/bold]\n{entry['error']}")
            console.print("---")

    except Exception as e:
        console.print(
            Panel(
                f"\n[red]Error:[/red] {str(e)}",
                title="SWAT CMD AI Error",
                border_style="red",
            )
        )
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
