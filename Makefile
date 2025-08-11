# AgentGen UV Wrapper Makefile
# Provides convenient shortcuts for common operations

.PHONY: help setup install-dev test clean demo status

# Default target
help: ## Show this help message
	@echo "🤖 AgentGen UV Wrapper - Available Commands:"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

setup: ## Setup the development environment with UV
	@echo "🔧 Setting up AgentGen with UV..."
	uv sync --dev
	@echo "✅ Setup complete!"

install-dev: setup ## Install development dependencies
	@echo "📦 Installing development dependencies..."
	uv sync --dev
	@echo "✅ Development dependencies installed!"

test: ## Run the demo and tests
	@echo "🧪 Running AgentGen demo..."
	uv run python demo_uv_wrapper.py

demo: ## Run the interactive demo
	@echo "🎬 Starting AgentGen UV Wrapper demo..."
	uv run python demo_uv_wrapper.py

status: ## Check system status
	@echo "🔍 Checking AgentGen system status..."
	uv run python -m agentgen.cli status --check-deps --check-git

clean: ## Clean build artifacts and cache
	@echo "🧹 Cleaning build artifacts..."
	rm -rf .venv __pycache__ *.egg-info build dist
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"

format: ## Format code with black and ruff
	@echo "🎨 Formatting code..."
	uv run black agentgen/
	uv run ruff check --fix agentgen/

lint: ## Lint code with ruff and mypy
	@echo "🔍 Linting code..."
	uv run ruff check agentgen/
	uv run mypy agentgen/ --ignore-missing-imports

# Quick commands using the wrapper
list-agents: ## List all available agents
	@./uv-wrapper.py list

list-profiles: ## List all available profiles  
	@./uv-wrapper.py profiles

# Development shortcuts
dev-setup: install-dev ## Full development setup
	@echo "🚀 Development environment ready!"
	@echo "💡 Try: make demo"

quick-test: ## Quick test of core functionality
	@echo "⚡ Quick test of UV wrapper..."
	@./uv-wrapper.py --version
	@./uv-wrapper.py status

# Installation shortcuts (require target directory)
install-all: ## Install all agents (usage: make install-all TARGET=/path/to/project)
	@if [ -z "$(TARGET)" ]; then \
		echo "❌ Please specify TARGET directory: make install-all TARGET=/path/to/project"; \
		exit 1; \
	fi
	@echo "🚀 Installing all agents to $(TARGET)..."
	@./uv-wrapper.py install $(TARGET) --all

install-simple: ## Install simple agents (usage: make install-simple TARGET=/path/to/project)
	@if [ -z "$(TARGET)" ]; then \
		echo "❌ Please specify TARGET directory: make install-simple TARGET=/path/to/project"; \
		exit 1; \
	fi
	@echo "🚀 Installing simple agents to $(TARGET)..."
	@./uv-wrapper.py install $(TARGET) --simple

# CI/CD friendly commands
ci-setup: ## Setup for CI/CD environments
	uv sync
	
ci-test: ## Run tests in CI/CD
	uv run python -c "import agentgen; print('✅ AgentGen package imports successfully')"
	uv run python -m agentgen.cli --version
	uv run python -m agentgen.cli status

# Build and package
build: ## Build the package
	@echo "📦 Building AgentGen package..."
	uv build
	@echo "✅ Build complete! Check dist/ directory"

# Information targets
info: ## Show project information
	@echo "📋 AgentGen Project Information:"
	@echo "  • Project: AgentGen UV Wrapper"
	@echo "  • Version: 0.2.0"
	@echo "  • UV Version: $(shell uv --version 2>/dev/null || echo 'Not installed')"
	@echo "  • Python: $(shell python3 --version 2>/dev/null || echo 'Not available')"
	@echo "  • Location: $(PWD)"

check-uv: ## Check if UV is properly installed
	@echo "🔍 Checking UV installation..."
	@if command -v uv >/dev/null 2>&1; then \
		echo "✅ UV is installed: $(shell uv --version)"; \
	else \
		echo "❌ UV is not installed"; \
		echo "📥 Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
		exit 1; \
	fi