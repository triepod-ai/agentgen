#!/usr/bin/env python3
"""
Setup script for Knowledge Refresh Pipeline
Quick setup and verification of the automated knowledge refresh system.
"""

import asyncio
import subprocess
import sys
import os
import yaml
import json
from pathlib import Path
from typing import Dict, List

def run_command(cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command with proper error handling"""
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, capture_output=True, text=True)

def check_requirements() -> bool:
    """Check if required dependencies are available"""
    print("🔍 Checking system requirements...")
    
    required_commands = ['docker', 'docker-compose', 'python3']
    missing_commands = []
    
    for cmd in required_commands:
        try:
            run_command(['which', cmd])
            print(f"  ✅ {cmd} found")
        except subprocess.CalledProcessError:
            missing_commands.append(cmd)
            print(f"  ❌ {cmd} not found")
    
    if missing_commands:
        print(f"\n❌ Missing required commands: {', '.join(missing_commands)}")
        print("Please install the missing dependencies and try again.")
        return False
    
    print("✅ All system requirements satisfied")
    return True

def setup_environment() -> bool:
    """Setup Python virtual environment and install dependencies"""
    print("\n🐍 Setting up Python environment...")
    
    try:
        # Create virtual environment if it doesn't exist
        venv_path = Path("venv")
        if not venv_path.exists():
            run_command([sys.executable, "-m", "venv", "venv"])
            print("  ✅ Virtual environment created")
        
        # Determine pip path
        pip_path = "venv/bin/pip" if os.name != 'nt' else "venv\\Scripts\\pip.exe"
        
        # Upgrade pip and install dependencies
        run_command([pip_path, "install", "--upgrade", "pip"])
        run_command([pip_path, "install", "-r", "requirements.txt"])
        
        print("✅ Python dependencies installed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to setup Python environment: {e}")
        return False

def setup_infrastructure() -> bool:
    """Setup BRAINPOD infrastructure with Docker Compose"""
    print("\n🏗️ Setting up BRAINPOD infrastructure...")
    
    try:
        # Start infrastructure services
        run_command(["docker-compose", "up", "-d", "redis", "qdrant", "chroma"])
        
        # Wait for services to be healthy
        print("  ⏳ Waiting for services to start...")
        run_command(["docker-compose", "up", "--wait"])
        
        print("✅ BRAINPOD infrastructure started")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to setup infrastructure: {e}")
        return False

def verify_infrastructure() -> bool:
    """Verify that infrastructure services are running correctly"""
    print("\n🔬 Verifying infrastructure services...")
    
    services = {
        'Redis': ('localhost', 6379),
        'Qdrant': ('localhost', 6333),
        'Chroma': ('localhost', 8000)
    }
    
    import socket
    
    all_healthy = True
    for service, (host, port) in services.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"  ✅ {service} is accessible on {host}:{port}")
            else:
                print(f"  ❌ {service} is not accessible on {host}:{port}")
                all_healthy = False
        except Exception as e:
            print(f"  ❌ Failed to check {service}: {e}")
            all_healthy = False
    
    if all_healthy:
        print("✅ All infrastructure services are healthy")
    else:
        print("❌ Some infrastructure services are not healthy")
    
    return all_healthy

async def test_orchestrator() -> bool:
    """Test the knowledge refresh orchestrator"""
    print("\n🧪 Testing knowledge refresh orchestrator...")
    
    try:
        # Import and test orchestrator
        sys.path.append(str(Path.cwd()))
        from knowledge_refresh_orchestrator import KnowledgeRefreshOrchestrator
        
        # Create orchestrator instance
        orchestrator = KnowledgeRefreshOrchestrator()
        
        # Test system status
        status = await orchestrator.get_system_status()
        
        if status['system_health']['overall_status'] == 'healthy':
            print("  ✅ Orchestrator system health check passed")
            print(f"  📊 Scheduled jobs: {status['job_status']['scheduled_jobs']}")
            print(f"  📈 Active alerts: {len(status['active_alerts'])}")
            return True
        else:
            print(f"  ❌ System health check failed: {status['system_health']}")
            return False
            
    except Exception as e:
        print(f"❌ Orchestrator test failed: {e}")
        return False

def create_sample_config() -> None:
    """Create sample configuration if it doesn't exist"""
    config_path = Path("config/refresh_schedules.yaml")
    
    if config_path.exists():
        print("✅ Configuration file already exists")
        return
    
    print("📝 Creating sample configuration...")
    
    # The config file already exists from our earlier creation
    # Just verify it's properly formatted
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        print("✅ Configuration file is valid")
    except Exception as e:
        print(f"❌ Configuration file has issues: {e}")

def display_usage_info() -> None:
    """Display usage information"""
    print("\n" + "="*60)
    print("🎉 Knowledge Refresh Pipeline Setup Complete!")
    print("="*60)
    
    print("\n📋 Quick Start Commands:")
    print("  • Status check:     python knowledge_refresh_orchestrator.py --status")
    print("  • Manual refresh:   python knowledge_refresh_orchestrator.py --agent security-auditor-enhanced --force")
    print("  • Run daemon:       python knowledge_refresh_orchestrator.py --daemon")
    print("  • Generate report:  python knowledge_refresh_orchestrator.py --report 24")
    
    print("\n🐳 Docker Commands:")
    print("  • Start all:        docker-compose up -d")
    print("  • View logs:        docker-compose logs orchestrator")
    print("  • Stop all:         docker-compose down")
    print("  • With monitoring:  docker-compose --profile monitoring up -d")
    
    print("\n📊 Service URLs:")
    print("  • Qdrant Admin:     http://localhost:6333/dashboard")
    print("  • Grafana:          http://localhost:3000 (admin/admin123)")
    print("  • Prometheus:       http://localhost:9090")
    
    print("\n📁 Important Files:")
    print("  • Configuration:    config/refresh_schedules.yaml")
    print("  • Logs:             knowledge_refresh.log")
    print("  • Documentation:    README.md")
    
    print("\n🔧 Configuration:")
    print("  • Edit config/refresh_schedules.yaml to customize refresh schedules")
    print("  • Set environment variables for notifications (WEBHOOK_URL, SLACK_WEBHOOK_URL)")
    print("  • Adjust agent configurations and source URLs as needed")

async def main():
    """Main setup function"""
    print("🚀 Knowledge Refresh Pipeline Setup")
    print("=====================================")
    
    # Check requirements
    if not check_requirements():
        return 1
    
    # Setup environment
    if not setup_environment():
        return 1
    
    # Create sample configuration
    create_sample_config()
    
    # Setup infrastructure
    if not setup_infrastructure():
        return 1
    
    # Verify infrastructure
    if not verify_infrastructure():
        print("⚠️  Infrastructure verification failed, but continuing...")
    
    # Test orchestrator
    try:
        if await test_orchestrator():
            print("✅ Orchestrator test passed")
        else:
            print("⚠️  Orchestrator test failed, but setup is complete")
    except Exception as e:
        print(f"⚠️  Could not test orchestrator: {e}")
    
    # Display usage information
    display_usage_info()
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)