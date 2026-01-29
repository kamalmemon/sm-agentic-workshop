# Agentic Workshop Demo

Marketing analytics dashboard for learning agentic coding with Claude Code.

## Quick Start

**Fresh laptop? Run bootstrap first:**
```bash
git clone https://github.com/kamalmemon/sm-agentic-workshop.git
cd sm-agentic-workshop
make bootstrap    # Installs uv, dependencies, sets up DB
make run          # Visit http://localhost:8000
```

**Already have uv installed?**
```bash
git clone https://github.com/kamalmemon/sm-agentic-workshop.git
cd sm-agentic-workshop
make install
make run
```

## Commands

```bash
make bootstrap     # First-time setup (installs uv if missing)
make install       # Install dependencies
make run           # Start dev server on port 8000
make run PORT=3000 # Start on custom port
make test          # Run tests
make verify        # Verify workshop setup
make reset-db      # Reset database
```

## Tech Stack

- Python 3.13, FastAPI
- htmx, Jinja2, Tailwind CSS
- Chart.js, SQLite, pytest
