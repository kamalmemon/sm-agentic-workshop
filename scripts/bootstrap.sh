#!/bin/bash
set -e

echo "=== Workshop Bootstrap ==="
echo "This script sets up everything from scratch."
echo ""

# Check OS
OS="$(uname -s)"
echo "Detected OS: $OS"

# Install uv if missing
if ! command -v uv &>/dev/null; then
    echo ""
    echo "Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    echo "✓ uv installed"
else
    echo "✓ uv already installed ($(uv --version))"
fi

# Check Python
if ! command -v python3 &>/dev/null; then
    echo ""
    echo "Python 3 not found. Please install Python 3.13+:"
    if [[ "$OS" == "Darwin" ]]; then
        echo "  brew install python@3.13"
    else
        echo "  sudo apt install python3.13  # or equivalent for your distro"
    fi
    exit 1
else
    echo "✓ Python installed ($(python3 --version))"
fi

# Install dependencies
echo ""
echo "Installing project dependencies..."
uv sync --all-extras
echo "✓ Dependencies installed"

# Initialize database
echo ""
echo "Setting up database..."
uv run python -c "from src.database import init_db, seed_db; init_db(); seed_db()"
echo "✓ Database ready"

# Run tests
echo ""
echo "Running tests..."
if uv run pytest --tb=short -q; then
    echo "✓ Tests passing"
else
    echo "✗ Tests failed - please check the output above"
    exit 1
fi

echo ""
echo "========================================="
echo "Bootstrap complete! You're ready to go."
echo ""
echo "Start the server with: make run"
echo "Or on a custom port:   make run PORT=3000"
echo "========================================="
