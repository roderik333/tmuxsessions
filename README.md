# tmuxsessions

A simple command line interface for saving and loading tmux sessions.

## Installation

```bash
python -m pip install --user 'git+https://github.com/roderik333/tmuxsessions.git#egg=tmuxsessions'
```

This will install a command `t` in your `~/.local/bin` directory.

## Usage

### Save Sessions

To save the current tmux sessions to a file, run:

```bash
t save-sessions
```

This will save the sessions to `~/.tmux_sessions.json`.

### Load Sessions

To load tmux sessions from a file, run:

```bash
t load-sessions
```

This will restore sessions that have been closed but does not restore single windows inside existing sessions.

## Autocoplete

We want tab completion, and we want it now.

```bash
eval "$(_T_COMPLETE=zsh_source t)"
```

This is for the zsh shell. For other shells look at [Shell Completion](https://click.palletsprojects.com/en/stable/shell-completion/).

## Aliases

Some useful aliases for `.zshrc`:

```bash
tm='tmux new -s '
tma='tmux attach-session -t '
tmd='tmux detach'
tml='tmux list-sessions'
tmc='tmux choose-tree'
```
