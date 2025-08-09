# Claude Code Sub-Agents Installation Guide

## Overview

The `install-agents` command provides a streamlined way to install and manage Claude Code sub-agents across your development environment. This comprehensive tool supports flexible agent installation, updates, and management.

## Installation Options

### Basic Usage
```bash
# Install all available agents
install-agents --all

# List available agents without installing
install-agents --list

# Perform a dry run to see what would be installed
install-agents --dry-run
```

### Advanced Installation Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--all` | Install all agents across categories | `install-agents --all` |
| `--list` | Show available agents without installing | `install-agents --list` |
| `--dry-run` | Simulate installation, show what would happen | `install-agents --dry-run` |
| `--force` | Force reinstallation of existing agents | `install-agents --force` |
| `--verbose` | Provide detailed installation logs | `install-agents --verbose` |
| `--skip-speak-check` | Skip text-to-speech configuration check | `install-agents --skip-speak-check` |

## Agent Categories

### 1. Development Agents
- Analyze, build, debug, review, and document code
- Best for software engineering workflows
- **Example**: `@build-backend`, `@review-code`

### 2. Infrastructure & DevOps
- Manage deployments, databases, environments
- Ideal for system configuration and monitoring
- **Example**: `@deploy-application`, `@configure-environment`

### 3. Data & AI
- Process data, train models, extract insights
- Perfect for data science and machine learning projects
- **Example**: `@process-data`, `@train-model`

### 4. Security Agents
- Conduct security audits, vulnerability assessments
- Critical for enterprise-level security compliance
- **Example**: `@secure-application`, `@security-specialist`

### 5. Specialized Tools
- Screenshot analysis, Git management, context export
- Targeted agents for specific technical tasks
- **Example**: `@manage-git`, `@analyze-screenshot`

## Real-World Usage Examples

### 1. New Project Setup
```bash
# Install all agents for a comprehensive toolkit
install-agents --all

# List agents to understand available capabilities
install-agents --list
```

### 2. Selective Installation
```bash
# Install only development and security agents
install-agents --dev --security
```

### 3. Update Existing Agents
```bash
# Force update all installed agents
install-agents --all --force

# Perform a dry run to preview updates
install-agents --all --dry-run --verbose
```

## Troubleshooting

### Common Issues

#### Agent Not Found
- **Symptom**: Specific agent doesn't appear after installation
- **Solution**: 
  1. Verify submodule is correctly initialized
  2. Check `/home/bryan/agentgen/submodules/claude-code-sub-agents`
  3. Run `install-agents --list` to confirm agent availability

#### Permission Errors
- **Symptom**: Permission denied during installation
- **Solution**:
  1. Use `sudo install-agents` if system-wide installation needed
  2. Check file permissions in agent directory
  3. Ensure script is executable: `chmod +x /home/bryan/bin/install-agents`

#### Text-to-Speech Configuration
- **Symptom**: Speak integration issues
- **Solution**: 
  1. Use `--skip-speak-check` if TTS setup is incomplete
  2. Configure speak command settings in `~/.bash_aliases`

## Best Practices

1. **Regular Updates**: Keep agents updated for latest features
2. **Selective Installation**: Install only necessary agents
3. **Dry Run First**: Always preview changes with `--dry-run`
4. **Force with Caution**: Use `--force` sparingly
5. **Verbose Mode**: Enable detailed logging during complex installations

## Configuration

Agents are managed via a git submodule at:
`/home/bryan/agentgen/submodules/claude-code-sub-agents`

Agent documentation is automatically updated in `CLAUDE.md` during installation.

## Support

For issues or agent suggestions:
- Check GitHub repository
- File an issue at support@claude.ai
- Join our developer community slack

---

**Tip**: The `install-agents` command is designed to be flexible, fast, and developer-friendly. Experiment and find the workflow that suits your needs!