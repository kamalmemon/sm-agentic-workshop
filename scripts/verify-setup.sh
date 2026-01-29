#!/bin/bash
set -e

PORT="${PORT:-8000}"

echo "Checking workshop prerequisites..."
echo ""

command -v claude &>/dev/null && echo "✓ Claude Code CLI" || { echo "✗ Claude Code CLI not found"; exit 1; }
command -v python3 &>/dev/null && echo "✓ Python $(python3 --version)" || { echo "✗ Python not found"; exit 1; }
command -v uv &>/dev/null && echo "✓ uv $(uv --version)" || { echo "✗ uv not found - run: make bootstrap"; exit 1; }

echo ""
echo "Installing dependencies..."
make install

echo ""
echo "Running tests..."
make test

echo ""
echo "Testing dev server on port $PORT..."
make run PORT=$PORT &
PID=$!
sleep 3
curl -s http://localhost:$PORT/health | grep -q "ok" && echo "✓ Dev server works" || { echo "✗ Server failed"; kill $PID 2>/dev/null; exit 1; }
kill $PID 2>/dev/null

echo ""
echo "========================================="
echo "All checks passed! Ready for workshop."
echo "========================================="
