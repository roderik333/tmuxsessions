"""A simple command line interface for saving sessions.

Based off of a bash script found on the internets.

I prefer to have these aliases in my .zshrc file:
tm='tmux new -s '
tma='tmux attach-session -t '
tmd='tmux detach'
tml='tmux list-sessions'

"""

import json
import os
import pathlib
import subprocess
from typing import TypeAlias, TypedDict, cast

import click


class Window(TypedDict):
    window_name: str
    path: str


Session: TypeAlias = dict[str, list[Window]]
SESSION_FILE = pathlib.Path.home() / ".tmux_sessions.json"


def execute_command(command: str, suppress_error: bool = False) -> str | None:
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if not suppress_error:
            click.secho(f"Error executing command: {e}", err=True, fg="red")
        return None


@click.command()
def save_sessions():
    """A simple way to save sessions.

    I don't use split windows so I wil not bother with implementing that.

    """
    command = "tmux list-windows -a -F '#S${d}#W${d}#{pane_current_path}'"
    output = execute_command(command)
    if output:
        sessions: Session = {}
        for line in output.splitlines():
            # Kept this since the original bash script used it.
            session_name, window_name, path = line.split("${d}")
            if session_name not in sessions:
                sessions[session_name] = []
            sessions[session_name].append({"window_name": window_name, "path": path})
        with open(SESSION_FILE, "w") as f:
            json.dump(sessions, f, indent=4)
        click.secho(f"Sessions saved to {SESSION_FILE}", fg="blue")


@click.command()
def load_sessions():
    """A simple way to load sessions.

    This will restore sessions that has been closed, but it will not resore single
    windows inside existings sessions.
    """

    if not os.path.exists(SESSION_FILE):
        click.echo(f"Session file {SESSION_FILE} not found.", err=True)
        return

    with open(SESSION_FILE, "r") as f:
        sessions: Session = cast("Session", json.load(f))

    existing_sessions: str | None = execute_command("tmux list-session -F '#S'", suppress_error=True)

    for session_name, windows in sessions.items():
        if existing_sessions is not None and session_name in existing_sessions:
            continue
        _ = execute_command(f"tmux new-session -d -s {session_name}")
        for window in windows:
            print(window["window_name"])
            _ = execute_command(f"tmux new-window -t {session_name} -n {window['window_name']} -c {window['path']}")

    click.secho("Sessions restored.", fg="green")


@click.group()
def cli():
    pass


cli.add_command(save_sessions)
cli.add_command(load_sessions)

if __name__ == "__main__":
    cli()
