# Agentic Workshop Demo

Marketing analytics dashboard for learning agentic coding with Claude Code.

## Quick Start

```bash
git clone https://github.com/kamalmemon/sm-agentic-workshop.git
cd sm-agentic-workshop
make bootstrap
make run
```

Open http://localhost:8000

## Commands

```bash
make bootstrap     # First-time setup (installs uv if missing)
make install       # Install dependencies
make run           # Start dev server on port 8000
make run PORT=3000 # Start on custom port
make test          # Run tests
make verify        # Verify setup
make reset-db      # Reset database
```

## Tech Stack

- Python 3.13, FastAPI
- htmx, Jinja2, Tailwind CSS
- Chart.js, SQLite, pytest
