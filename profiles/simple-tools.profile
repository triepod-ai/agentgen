name: simple-tools
description: Ultra-fast single-tool agents optimized for specific tasks with minimal loading time
agents:
  # Read Agents (Analyzers)
  - config-reader
  - log-reader
  - readme-reader
  - env-reader
  - analyze-screenshot
  
  # Write Agents (Generators)
  - gitignore-writer
  - readme-writer
  - env-writer
  - changelog-writer
  
  # Bash Agents (Executors)
  - test-runner
  - build-runner
  - git-executor
  - dependency-installer
  
  # Grep Agents (Searchers)
  - error-finder
  - todo-finder
  - import-finder
  - function-finder
  
  # Edit Agents (Modifiers)
  - comment-remover
  - whitespace-fixer
  - import-sorter
  - typo-fixer