# Codra

local-first ai coding assistant. runs 100% offline with ollama.
no cloud. no telemetry. just python + llm.

## Installation

1. clone the repo:
   ```
   git clone https://github.com/sidharthsreelal/codra.git
   cd codra
   ```
2. no pip requirements needed (standard library only).

## Setup

1. install ollama (ollama.com)
2. get a model:
   ```
   ollama pull llama3.2
   ```
   (or deepseek-coder, mistral, whatever)
3. run it:
   ```
   python run.py
   ```

## How it works

it's got 4 agents running inside:
- **planner**: breaks stuff down
- **coder**: writes the messy python
- **runner**: execs terminal commands
- **reviewer**: makes sure it works

they talk to each other over a local message bus.
everything is stored in `~/.codra`.

## Commands

- `help`         - show commands
- `model <name>` - switch model (e.g. `model mistral`)
- `new`          - start fresh session
- `sessions`     - list old sessions
- `quick`        - fast chat (no agents)
- `clear`        - wipe screen
- `quit`         - bye

## Troubleshooting

**ollama connection error?**
make sure `ollama serve` is running in another terminal.

**code fails?**
it happens. tell codra to fix it. it usually figures it out.

**files?**
- `brain/` - agent logic
- `tools/` - fs/shell stuff
- `loop.py` - main loop
- `mem.py` - save/load

hack it if you want. license: do whatever.
