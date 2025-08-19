# src/analysis/domain_detector.py
import time
from abc import ABC, abstractmethod
from typing import Dict, List
import re

class DomainProcessor(ABC):
    def __init__(self, domain_name: str, complexity_bias: float, preferred_agents: List[str]):
        self.domain_name = domain_name
        self.complexity_bias = complexity_bias
        self.preferred_agents = preferred_agents
        
    @abstractmethod
    def analyze(self, task_description: str) -> float:
        """Return confidence score for domain detection (0.0-1.0)"""
        pass

class FrontendDomainProcessor(DomainProcessor):
    def __init__(self):
        super().__init__(
            "frontend", 
            0.7, 
            ["@build-frontend", "@frontend-developer", "@ui-designer"]
        )
        self.keywords = {
            'primary': ['react', 'vue', 'angular', 'frontend', 'ui', 'component', 'jsx', 'tsx'],
            'secondary': ['css', 'responsive', 'styling', 'layout', 'design', 'interface'],
            'frameworks': ['nextjs', 'nuxt', 'svelte', 'gatsby', 'webpack', 'vite']
        }
        self.file_patterns = [
            r'.*\.(jsx|tsx|vue|svelte)$',
            r'.*\.(css|scss|sass|less)$',
            r'.*\.(html|htm)$'
        ]
    
    def analyze(self, task_description: str) -> float:
        tokens = task_description.lower().split()
        token_count = len(tokens) if tokens else 1
        
        # Fast keyword matching with better scoring
        primary_matches = sum(1 for token in tokens if token in self.keywords['primary'])
        secondary_matches = sum(1 for token in tokens if token in self.keywords['secondary'])
        framework_matches = sum(1 for token in tokens if token in self.keywords['frameworks'])
        
        # File pattern matching
        pattern_matches = sum(1 for pattern in self.file_patterns 
                            if re.search(pattern, task_description, re.IGNORECASE))
        
        # Calculate confidence with improved weights
        keyword_score = (primary_matches * 0.6 + secondary_matches * 0.4 + 
                        framework_matches * 0.5) / token_count
        pattern_score = min(pattern_matches * 0.3, 0.4)
        
        total_confidence = min(keyword_score + pattern_score, 0.95)
        
        # Bonus for common frontend combinations
        if primary_matches > 0 and secondary_matches > 0:
            total_confidence = min(total_confidence * 1.3, 0.95)
        
        # Lower threshold for better detection
        return total_confidence if total_confidence > 0.1 else 0.0

class BackendDomainProcessor(DomainProcessor):
    def __init__(self):
        super().__init__(
            "backend", 
            0.8, 
            ["@build-backend", "@backend-architect", "@database-specialist"]
        )
        self.keywords = {
            'primary': ['api', 'server', 'backend', 'database', 'endpoint', 'service'],
            'secondary': ['auth', 'authentication', 'middleware', 'controller', 'model'],
            'technologies': ['nodejs', 'python', 'django', 'flask', 'express', 'fastapi']
        }
    
    def analyze(self, task_description: str) -> float:
        tokens = task_description.lower().split()
        token_count = len(tokens) if tokens else 1
        
        primary_matches = sum(1 for token in tokens if token in self.keywords['primary'])
        secondary_matches = sum(1 for token in tokens if token in self.keywords['secondary'])
        tech_matches = sum(1 for token in tokens if token in self.keywords['technologies'])
        
        keyword_score = (primary_matches * 0.6 + secondary_matches * 0.4 + 
                        tech_matches * 0.5) / token_count
        
        return min(keyword_score, 0.95) if keyword_score > 0.1 else 0.0

class SecurityDomainProcessor(DomainProcessor):
    def __init__(self):
        super().__init__(
            "security", 
            0.9, 
            ["@security-auditor", "@secure-application"]
        )
        self.keywords = {
            'primary': ['security', 'auth', 'authentication', 'authorization', 'vulnerability'],
            'secondary': ['audit', 'secure', 'encrypt', 'decrypt', 'token', 'jwt'],
            'threats': ['xss', 'csrf', 'injection', 'breach', 'attack', 'threat']
        }
    
    def analyze(self, task_description: str) -> float:
        tokens = task_description.lower().split()
        token_count = len(tokens) if tokens else 1
        
        primary_matches = sum(1 for token in tokens if token in self.keywords['primary'])
        secondary_matches = sum(1 for token in tokens if token in self.keywords['secondary'])
        threat_matches = sum(1 for token in tokens if token in self.keywords['threats'])
        
        keyword_score = (primary_matches * 0.7 + secondary_matches * 0.5 + 
                        threat_matches * 0.6) / token_count
        
        return min(keyword_score, 0.95) if keyword_score > 0.08 else 0.0

class InfrastructureDomainProcessor(DomainProcessor):
    def __init__(self):
        super().__init__(
            "infrastructure", 
            0.8, 
            ["@deploy-application", "@deployment-engineer", "@manage-database"]
        )
        self.keywords = {
            'primary': ['deploy', 'deployment', 'infrastructure', 'docker', 'container', 'cloud', 'aws'],
            'secondary': ['ci/cd', 'pipeline', 'kubernetes', 'helm', 'terraform'],
            'operations': ['monitor', 'scale', 'backup', 'restore', 'migrate']
        }
    
    def analyze(self, task_description: str) -> float:
        tokens = task_description.lower().split()
        token_count = len(tokens) if tokens else 1
        
        # Use substring matching for compound words like "deployment"
        primary_matches = sum(1 for token in tokens 
                            if any(keyword in token for keyword in self.keywords['primary']))
        secondary_matches = sum(1 for token in tokens if token in self.keywords['secondary'])
        ops_matches = sum(1 for token in tokens if token in self.keywords['operations'])
        
        keyword_score = (primary_matches * 0.6 + secondary_matches * 0.4 + 
                        ops_matches * 0.3) / token_count
        
        return min(keyword_score, 0.95) if keyword_score > 0.1 else 0.0

class TestingDomainProcessor(DomainProcessor):
    def __init__(self):
        super().__init__(
            "testing", 
            0.6, 
            ["@test-automation", "@qa-expert", "@test-automator"]
        )
        self.keywords = {
            'primary': ['test', 'testing', 'qa', 'quality', 'validation'],
            'secondary': ['unit', 'integration', 'e2e', 'coverage', 'mock'],
            'frameworks': ['jest', 'pytest', 'cypress', 'selenium', 'mocha']
        }
    
    def analyze(self, task_description: str) -> float:
        tokens = task_description.lower().split()
        token_count = len(tokens) if tokens else 1
        
        primary_matches = sum(1 for token in tokens if token in self.keywords['primary'])
        secondary_matches = sum(1 for token in tokens if token in self.keywords['secondary'])
        framework_matches = sum(1 for token in tokens if token in self.keywords['frameworks'])
        
        keyword_score = (primary_matches * 0.6 + secondary_matches * 0.4 + 
                        framework_matches * 0.3) / token_count
        
        return min(keyword_score, 0.95) if keyword_score > 0.1 else 0.0

class DocumentationDomainProcessor(DomainProcessor):
    def __init__(self):
        super().__init__(
            "documentation", 
            0.5, 
            ["@generate-documentation", "@documentation-expert", "@write-content"]
        )
        self.keywords = {
            'primary': ['document', 'documentation', 'readme', 'guide', 'manual'],
            'secondary': ['wiki', 'docs', 'api-doc', 'tutorial', 'example'],
            'actions': ['write', 'create', 'generate', 'update', 'maintain']
        }
    
    def analyze(self, task_description: str) -> float:
        tokens = task_description.lower().split()
        token_count = len(tokens) if tokens else 1
        
        primary_matches = sum(1 for token in tokens if token in self.keywords['primary'])
        secondary_matches = sum(1 for token in tokens if token in self.keywords['secondary'])
        action_matches = sum(1 for token in tokens if token in self.keywords['actions'])
        
        keyword_score = (primary_matches * 0.7 + secondary_matches * 0.5 + 
                        action_matches * 0.2) / token_count
        
        return min(keyword_score, 0.95) if keyword_score > 0.15 else 0.0

class DomainDetectionEngine:
    def __init__(self):
        self.processors = {
            'frontend': FrontendDomainProcessor(),
            'backend': BackendDomainProcessor(),
            'security': SecurityDomainProcessor(),
            'infrastructure': InfrastructureDomainProcessor(),
            'testing': TestingDomainProcessor(),
            'documentation': DocumentationDomainProcessor()
        }
        # Performance target: contribute <10ms to total routing time
    
    def detect_domains(self, task_description: str) -> Dict:
        """Detect all applicable domains for the task with performance monitoring"""
        
        start_time = time.perf_counter()
        
        detected_domains = []
        total_confidence = 0
        
        # Run all processors (parallel in future optimization)
        for domain_name, processor in self.processors.items():
            confidence = processor.analyze(task_description)
            if confidence > 0.1:  # Even lower threshold for better detection
                detected_domains.append({
                    'domain': domain_name,
                    'confidence': confidence,
                    'complexity_bias': processor.complexity_bias,
                    'preferred_agents': processor.preferred_agents
                })
                total_confidence += confidence
        
        # Sort by confidence for routing priority
        detected_domains.sort(key=lambda x: x['confidence'], reverse=True)
        
        analysis_time_ms = (time.perf_counter() - start_time) * 1000
        
        return {
            'domains': detected_domains,
            'domain_count': len(detected_domains),
            'total_confidence': total_confidence,
            'primary_domain': detected_domains[0]['domain'] if detected_domains else None,
            'analysis_time_ms': analysis_time_ms
        }