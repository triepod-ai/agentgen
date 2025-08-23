#!/usr/bin/env python3
"""
Source Monitor - Automated Source Change Detection and Knowledge Extraction
Part of the knowledge refresh pipeline for enhanced agents.
"""

import asyncio
import logging
import aiohttp
import feedparser
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import hashlib
import re
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import time

logger = logging.getLogger(__name__)

@dataclass
class SourceInfo:
    """Information about a knowledge source"""
    source_id: str
    url: str
    source_type: str  # 'documentation', 'blog', 'api', 'rss', 'github'
    credibility_score: float
    update_frequency: str  # 'daily', 'weekly', 'monthly'
    last_checked: Optional[datetime] = None
    last_modified: Optional[datetime] = None
    content_hash: Optional[str] = None
    metadata: Dict[str, Any] = None

@dataclass
class KnowledgePoint:
    """Individual piece of knowledge extracted from sources"""
    content: str
    source_id: str
    source_url: str
    knowledge_type: str
    domain: str
    credibility_score: float
    extraction_timestamp: datetime
    metadata: Dict[str, Any] = None

class SourceMonitor:
    """
    Monitors knowledge sources for changes and extracts structured knowledge.
    Supports various source types including documentation, blogs, APIs, and RSS feeds.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize source monitor with configuration"""
        self.config = config or {}
        
        # HTTP client configuration
        self.session_timeout = aiohttp.ClientTimeout(
            total=self.config.get('timeout', 30),
            connect=self.config.get('connect_timeout', 10)
        )
        
        # Source configurations
        self.source_configs = self._load_source_configs()
        
        # Content extraction patterns
        self.extraction_patterns = self._load_extraction_patterns()
        
        # Rate limiting configuration
        self.rate_limits = self.config.get('rate_limits', {
            'requests_per_second': 2,
            'burst_limit': 5,
            'delay_between_requests': 0.5
        })
        
        logger.info("SourceMonitor initialized for automated change detection")

    async def check_source_changes(self, sources: List[str]) -> bool:
        """Check if sources have changes requiring refresh"""
        logger.info(f"Checking {len(sources)} sources for changes")
        
        # Simulate source change detection
        await asyncio.sleep(0.1)
        
        # Return True to simulate changes detected
        return True

    def _load_source_configs(self) -> Dict[str, SourceInfo]:
        """Load source configurations from config"""
        configs = {}
        
        # Default source configurations
        default_sources = {
            'owasp_top_10': SourceInfo(
                source_id='owasp_top_10',
                url='https://owasp.org/www-project-top-ten/',
                source_type='documentation',
                credibility_score=1.0,
                update_frequency='monthly',
                metadata={
                    'domain': 'security',
                    'content_selectors': ['.main-content', 'article', '.content'],
                    'knowledge_types': ['vulnerability_patterns', 'security_guidelines']
                }
            ),
            'react_docs': SourceInfo(
                source_id='react_docs',
                url='https://react.dev/learn',
                source_type='documentation',
                credibility_score=0.98,
                update_frequency='weekly',
                metadata={
                    'domain': 'frontend',
                    'content_selectors': ['.main-content', 'article', '.markdown-body'],
                    'knowledge_types': ['component_patterns', 'best_practices', 'api_reference']
                }
            ),
            'nist_cybersecurity': SourceInfo(
                source_id='nist_cybersecurity',
                url='https://www.nist.gov/cyberframework',
                source_type='documentation',
                credibility_score=0.99,
                update_frequency='quarterly',
                metadata={
                    'domain': 'security',
                    'content_selectors': ['.field--name-body', '.main-content'],
                    'knowledge_types': ['compliance_frameworks', 'security_standards']
                }
            ),
            'cve_database': SourceInfo(
                source_id='cve_database',
                url='https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=',
                source_type='api',
                credibility_score=1.0,
                update_frequency='daily',
                metadata={
                    'domain': 'security',
                    'api_format': 'xml',
                    'knowledge_types': ['vulnerability_details', 'cve_references']
                }
            )
        }
        
        # Merge with user-provided configurations
        user_sources = self.config.get('sources', {})
        for source_id, source_config in user_sources.items():
            if isinstance(source_config, dict):
                configs[source_id] = SourceInfo(**source_config)
            else:
                configs[source_id] = source_config
        
        # Add default sources if not overridden
        for source_id, source_info in default_sources.items():
            if source_id not in configs:
                configs[source_id] = source_info
        
        return configs

    def _load_extraction_patterns(self) -> Dict[str, Dict]:
        """Load content extraction patterns by domain and source type"""
        return {
            'security': {
                'vulnerability_patterns': [
                    r'CVE-\d{4}-\d{4,7}',  # CVE identifiers
                    r'CWE-\d+',            # CWE identifiers
                    r'CVSS:\d+\.\d+',      # CVSS scores
                ],
                'security_concepts': [
                    r'authentication',
                    r'authorization',
                    r'encryption',
                    r'injection',
                    r'cross-site scripting',
                    r'SQL injection',
                    r'privilege escalation'
                ]
            },
            'frontend': {
                'react_patterns': [
                    r'use\w+\(',           # React hooks
                    r'React\.\w+',         # React API calls
                    r'useState|useEffect|useContext|useReducer',  # Common hooks
                ],
                'component_patterns': [
                    r'function\s+\w+Component',
                    r'const\s+\w+\s*=\s*\(\s*\)\s*=>',  # Arrow function components
                    r'export\s+default\s+function'
                ]
            },
            'backend': {
                'api_patterns': [
                    r'GET|POST|PUT|DELETE|PATCH',  # HTTP methods
                    r'\/api\/v\d+\/',              # API versioning
                    r'@\w+\(',                     # Decorators
                ],
                'database_patterns': [
                    r'SELECT|INSERT|UPDATE|DELETE',
                    r'CREATE\s+TABLE',
                    r'INDEX|PRIMARY\s+KEY|FOREIGN\s+KEY'
                ]
            }
        }

    async def check_source_changes(self, source_id: str) -> Dict[str, Any]:
        """Check if a source has changes requiring knowledge refresh"""
        if source_id not in self.source_configs:
            logger.error(f"Unknown source ID: {source_id}")
            return {'has_changes': False, 'error': 'Unknown source'}
        
        source_info = self.source_configs[source_id]
        
        try:
            logger.info(f"Checking changes for source {source_id}: {source_info.url}")
            
            # Check for changes based on source type
            if source_info.source_type == 'documentation':
                return await self._check_documentation_changes(source_info)
            elif source_info.source_type == 'rss':
                return await self._check_rss_changes(source_info)
            elif source_info.source_type == 'api':
                return await self._check_api_changes(source_info)
            elif source_info.source_type == 'github':
                return await self._check_github_changes(source_info)
            else:
                return await self._check_generic_changes(source_info)
                
        except Exception as e:
            logger.error(f"Failed to check changes for source {source_id}: {str(e)}")
            return {
                'has_changes': False,
                'error': str(e),
                'freshness_score': 0.0,
                'last_checked': datetime.utcnow().isoformat()
            }

    async def _check_documentation_changes(self, source_info: SourceInfo) -> Dict[str, Any]:
        """Check changes in documentation sources"""
        async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
            try:
                async with session.get(source_info.url) as response:
                    if response.status != 200:
                        return {
                            'has_changes': False,
                            'error': f'HTTP {response.status}',
                            'freshness_score': 0.0
                        }
                    
                    content = await response.text()
                    
                    # Calculate content hash
                    current_hash = hashlib.md5(content.encode()).hexdigest()
                    
                    # Check if content has changed
                    has_changes = (
                        source_info.content_hash is None or 
                        source_info.content_hash != current_hash
                    )
                    
                    # Calculate freshness score
                    last_modified = response.headers.get('Last-Modified')
                    freshness_score = self._calculate_freshness_score(last_modified)
                    
                    # Extract change summary if there are changes
                    changes = {}
                    if has_changes:
                        changes = await self._analyze_content_changes(source_info, content)
                    
                    # Update source info
                    source_info.content_hash = current_hash
                    source_info.last_checked = datetime.utcnow()
                    if last_modified:
                        try:
                            source_info.last_modified = datetime.strptime(
                                last_modified, '%a, %d %b %Y %H:%M:%S %Z'
                            )
                        except:
                            pass
                    
                    return {
                        'has_changes': has_changes,
                        'freshness_score': freshness_score,
                        'content_hash': current_hash,
                        'changes': changes,
                        'last_checked': source_info.last_checked.isoformat(),
                        'content_size': len(content)
                    }
                    
            except aiohttp.ClientError as e:
                logger.error(f"Network error checking {source_info.source_id}: {str(e)}")
                return {
                    'has_changes': False,
                    'error': f'Network error: {str(e)}',
                    'freshness_score': 0.0
                }

    async def _check_rss_changes(self, source_info: SourceInfo) -> Dict[str, Any]:
        """Check changes in RSS feed sources"""
        try:
            # Download RSS feed
            async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
                async with session.get(source_info.url) as response:
                    if response.status != 200:
                        return {
                            'has_changes': False,
                            'error': f'HTTP {response.status}',
                            'freshness_score': 0.0
                        }
                    
                    rss_content = await response.text()
            
            # Parse RSS feed
            feed = feedparser.parse(rss_content)
            
            # Check for new entries since last check
            has_changes = False
            new_entries = []
            
            if source_info.last_checked:
                for entry in feed.entries:
                    # Parse entry date
                    entry_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        entry_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        entry_date = datetime(*entry.updated_parsed[:6])
                    
                    if entry_date and entry_date > source_info.last_checked:
                        has_changes = True
                        new_entries.append({
                            'title': entry.get('title', ''),
                            'link': entry.get('link', ''),
                            'published': entry_date.isoformat(),
                            'summary': entry.get('summary', '')
                        })
            else:
                # First time checking - consider all recent entries as new
                has_changes = len(feed.entries) > 0
                for entry in feed.entries[:5]:  # Limit to 5 most recent
                    entry_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        entry_date = datetime(*entry.published_parsed[:6])
                    
                    new_entries.append({
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry_date.isoformat() if entry_date else '',
                        'summary': entry.get('summary', '')
                    })
            
            # Calculate freshness score based on most recent entry
            freshness_score = 0.0
            if feed.entries and hasattr(feed.entries[0], 'published_parsed'):
                most_recent = datetime(*feed.entries[0].published_parsed[:6])
                freshness_score = self._calculate_freshness_score_from_datetime(most_recent)
            
            # Update source info
            source_info.last_checked = datetime.utcnow()
            
            return {
                'has_changes': has_changes,
                'freshness_score': freshness_score,
                'new_entries_count': len(new_entries),
                'new_entries': new_entries,
                'total_entries': len(feed.entries),
                'feed_title': feed.feed.get('title', ''),
                'last_checked': source_info.last_checked.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to check RSS changes for {source_info.source_id}: {str(e)}")
            return {
                'has_changes': False,
                'error': str(e),
                'freshness_score': 0.0
            }

    async def _check_api_changes(self, source_info: SourceInfo) -> Dict[str, Any]:
        """Check changes in API sources"""
        # For now, implement basic API change detection
        # In practice, this would be more sophisticated based on API type
        return await self._check_generic_changes(source_info)

    async def _check_github_changes(self, source_info: SourceInfo) -> Dict[str, Any]:
        """Check changes in GitHub repository sources"""
        # Extract owner and repo from GitHub URL
        url_parts = urlparse(source_info.url)
        path_parts = url_parts.path.strip('/').split('/')
        
        if len(path_parts) < 2:
            return {
                'has_changes': False,
                'error': 'Invalid GitHub URL format',
                'freshness_score': 0.0
            }
        
        owner, repo = path_parts[0], path_parts[1]
        
        try:
            # Check repository commits via GitHub API
            api_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
            
            async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
                headers = {}
                github_token = self.config.get('github_token')
                if github_token:
                    headers['Authorization'] = f'token {github_token}'
                
                async with session.get(api_url, headers=headers) as response:
                    if response.status != 200:
                        return {
                            'has_changes': False,
                            'error': f'GitHub API error: HTTP {response.status}',
                            'freshness_score': 0.0
                        }
                    
                    commits = await response.json()
                    
                    if not commits:
                        return {
                            'has_changes': False,
                            'freshness_score': 0.0,
                            'commits_checked': 0
                        }
                    
                    # Check for new commits since last check
                    has_changes = False
                    new_commits = []
                    
                    for commit in commits[:10]:  # Check last 10 commits
                        commit_date = datetime.fromisoformat(
                            commit['commit']['author']['date'].replace('Z', '+00:00')
                        ).replace(tzinfo=None)
                        
                        if (source_info.last_checked is None or 
                            commit_date > source_info.last_checked):
                            has_changes = True
                            new_commits.append({
                                'sha': commit['sha'][:7],
                                'message': commit['commit']['message'].split('\n')[0],
                                'author': commit['commit']['author']['name'],
                                'date': commit_date.isoformat()
                            })
                    
                    # Calculate freshness score from most recent commit
                    most_recent_commit = datetime.fromisoformat(
                        commits[0]['commit']['author']['date'].replace('Z', '+00:00')
                    ).replace(tzinfo=None)
                    freshness_score = self._calculate_freshness_score_from_datetime(most_recent_commit)
                    
                    # Update source info
                    source_info.last_checked = datetime.utcnow()
                    
                    return {
                        'has_changes': has_changes,
                        'freshness_score': freshness_score,
                        'new_commits_count': len(new_commits),
                        'new_commits': new_commits,
                        'repository': f"{owner}/{repo}",
                        'last_checked': source_info.last_checked.isoformat()
                    }
                    
        except Exception as e:
            logger.error(f"Failed to check GitHub changes for {source_info.source_id}: {str(e)}")
            return {
                'has_changes': False,
                'error': str(e),
                'freshness_score': 0.0
            }

    async def _check_generic_changes(self, source_info: SourceInfo) -> Dict[str, Any]:
        """Generic change detection for various source types"""
        async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
            try:
                async with session.head(source_info.url) as response:
                    if response.status != 200:
                        # Fall back to GET request
                        async with session.get(source_info.url) as get_response:
                            if get_response.status != 200:
                                return {
                                    'has_changes': False,
                                    'error': f'HTTP {get_response.status}',
                                    'freshness_score': 0.0
                                }
                            response = get_response
                    
                    # Check Last-Modified header
                    last_modified = response.headers.get('Last-Modified')
                    etag = response.headers.get('ETag')
                    
                    # Determine if there are changes
                    has_changes = True  # Default to assuming changes for new sources
                    
                    if source_info.last_modified and last_modified:
                        try:
                            current_modified = datetime.strptime(
                                last_modified, '%a, %d %b %Y %H:%M:%S %Z'
                            )
                            has_changes = current_modified > source_info.last_modified
                        except:
                            pass
                    
                    # Calculate freshness score
                    freshness_score = self._calculate_freshness_score(last_modified)
                    
                    # Update source info
                    source_info.last_checked = datetime.utcnow()
                    if last_modified:
                        try:
                            source_info.last_modified = datetime.strptime(
                                last_modified, '%a, %d %b %Y %H:%M:%S %Z'
                            )
                        except:
                            pass
                    
                    return {
                        'has_changes': has_changes,
                        'freshness_score': freshness_score,
                        'last_modified': last_modified,
                        'etag': etag,
                        'last_checked': source_info.last_checked.isoformat()
                    }
                    
            except Exception as e:
                logger.error(f"Generic check failed for {source_info.source_id}: {str(e)}")
                return {
                    'has_changes': False,
                    'error': str(e),
                    'freshness_score': 0.0
                }

    async def extract_collection_knowledge(self, collection_id: str, source_ids: List[str]) -> Dict[str, Any]:
        """Extract knowledge from specified sources for a collection"""
        logger.info(f"Extracting knowledge for collection {collection_id} from {len(source_ids)} sources")
        
        collection_knowledge = {
            'collection_id': collection_id,
            'knowledge_points': [],
            'point_count': 0,
            'new_count': 0,
            'updated_count': 0,
            'source_summary': {},
            'extraction_timestamp': datetime.utcnow().isoformat()
        }
        
        # Process each source
        for source_id in source_ids:
            if source_id not in self.source_configs:
                logger.warning(f"Unknown source ID: {source_id}")
                continue
            
            source_info = self.source_configs[source_id]
            
            try:
                # Extract knowledge from this source
                source_knowledge = await self._extract_source_knowledge(source_info, collection_id)
                
                # Add to collection knowledge
                collection_knowledge['knowledge_points'].extend(source_knowledge['knowledge_points'])
                collection_knowledge['new_count'] += source_knowledge['new_count']
                collection_knowledge['updated_count'] += source_knowledge['updated_count']
                
                # Track source summary
                collection_knowledge['source_summary'][source_id] = {
                    'points_extracted': source_knowledge['point_count'],
                    'extraction_status': 'success',
                    'source_url': source_info.url
                }
                
            except Exception as e:
                logger.error(f"Failed to extract knowledge from source {source_id}: {str(e)}")
                collection_knowledge['source_summary'][source_id] = {
                    'points_extracted': 0,
                    'extraction_status': 'failed',
                    'error': str(e),
                    'source_url': source_info.url
                }
        
        collection_knowledge['point_count'] = len(collection_knowledge['knowledge_points'])
        
        logger.info(f"Extracted {collection_knowledge['point_count']} knowledge points for collection {collection_id}")
        return collection_knowledge

    async def _extract_source_knowledge(self, source_info: SourceInfo, collection_id: str) -> Dict[str, Any]:
        """Extract structured knowledge from a specific source"""
        knowledge_points = []
        
        try:
            # Get source content
            async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
                await asyncio.sleep(self.rate_limits['delay_between_requests'])  # Rate limiting
                
                async with session.get(source_info.url) as response:
                    if response.status != 200:
                        raise Exception(f"HTTP {response.status}")
                    
                    content = await response.text()
            
            # Extract knowledge based on source type and domain
            if source_info.source_type == 'documentation':
                knowledge_points = await self._extract_documentation_knowledge(
                    source_info, content, collection_id
                )
            elif source_info.source_type == 'rss':
                knowledge_points = await self._extract_rss_knowledge(
                    source_info, content, collection_id
                )
            else:
                knowledge_points = await self._extract_generic_knowledge(
                    source_info, content, collection_id
                )
            
            return {
                'source_id': source_info.source_id,
                'knowledge_points': knowledge_points,
                'point_count': len(knowledge_points),
                'new_count': len(knowledge_points),  # For simplicity, treat all as new
                'updated_count': 0,
                'extraction_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Knowledge extraction failed for {source_info.source_id}: {str(e)}")
            return {
                'source_id': source_info.source_id,
                'knowledge_points': [],
                'point_count': 0,
                'new_count': 0,
                'updated_count': 0,
                'error': str(e)
            }

    async def _extract_documentation_knowledge(self, source_info: SourceInfo, content: str, collection_id: str) -> List[KnowledgePoint]:
        """Extract knowledge from documentation sources"""
        knowledge_points = []
        
        # Parse HTML content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Get content selectors from source metadata
        selectors = source_info.metadata.get('content_selectors', ['body'])
        domain = source_info.metadata.get('domain', 'general')
        knowledge_types = source_info.metadata.get('knowledge_types', ['general'])
        
        # Extract content from specified selectors
        for selector in selectors:
            elements = soup.select(selector)
            
            for element in elements:
                # Extract text content
                text_content = element.get_text(strip=True)
                
                if len(text_content) < 50:  # Skip very short content
                    continue
                
                # Split into chunks if content is very long
                chunks = self._split_content_into_chunks(text_content)
                
                for chunk in chunks:
                    # Determine knowledge type based on content patterns
                    knowledge_type = self._classify_knowledge_type(chunk, domain, knowledge_types)
                    
                    knowledge_point = KnowledgePoint(
                        content=chunk,
                        source_id=source_info.source_id,
                        source_url=source_info.url,
                        knowledge_type=knowledge_type,
                        domain=domain,
                        credibility_score=source_info.credibility_score,
                        extraction_timestamp=datetime.utcnow(),
                        metadata={
                            'element_tag': element.name,
                            'collection_id': collection_id,
                            'extraction_method': 'documentation_parser'
                        }
                    )
                    
                    knowledge_points.append(knowledge_point)
        
        # Extract code examples if present
        code_elements = soup.find_all(['code', 'pre'])
        for code_element in code_elements:
            code_content = code_element.get_text(strip=True)
            
            if len(code_content) > 20:  # Only meaningful code snippets
                knowledge_point = KnowledgePoint(
                    content=code_content,
                    source_id=source_info.source_id,
                    source_url=source_info.url,
                    knowledge_type='code_example',
                    domain=domain,
                    credibility_score=source_info.credibility_score,
                    extraction_timestamp=datetime.utcnow(),
                    metadata={
                        'element_tag': code_element.name,
                        'collection_id': collection_id,
                        'extraction_method': 'code_extractor'
                    }
                )
                
                knowledge_points.append(knowledge_point)
        
        return knowledge_points

    async def _extract_rss_knowledge(self, source_info: SourceInfo, content: str, collection_id: str) -> List[KnowledgePoint]:
        """Extract knowledge from RSS feed sources"""
        knowledge_points = []
        
        # Parse RSS feed
        feed = feedparser.parse(content)
        
        domain = source_info.metadata.get('domain', 'general')
        
        for entry in feed.entries:
            # Extract title and summary
            title = entry.get('title', '')
            summary = entry.get('summary', '')
            link = entry.get('link', source_info.url)
            
            # Combine title and summary
            full_content = f"{title}\n\n{summary}" if summary else title
            
            if len(full_content.strip()) < 20:
                continue
            
            knowledge_point = KnowledgePoint(
                content=full_content,
                source_id=source_info.source_id,
                source_url=link,
                knowledge_type='article',
                domain=domain,
                credibility_score=source_info.credibility_score,
                extraction_timestamp=datetime.utcnow(),
                metadata={
                    'title': title,
                    'link': link,
                    'published': entry.get('published', ''),
                    'collection_id': collection_id,
                    'extraction_method': 'rss_parser'
                }
            )
            
            knowledge_points.append(knowledge_point)
        
        return knowledge_points

    async def _extract_generic_knowledge(self, source_info: SourceInfo, content: str, collection_id: str) -> List[KnowledgePoint]:
        """Extract knowledge from generic sources"""
        knowledge_points = []
        
        # Basic text extraction for generic sources
        soup = BeautifulSoup(content, 'html.parser')
        text_content = soup.get_text(strip=True)
        
        if len(text_content) < 100:
            return knowledge_points
        
        # Split into meaningful chunks
        chunks = self._split_content_into_chunks(text_content)
        domain = source_info.metadata.get('domain', 'general') if source_info.metadata else 'general'
        
        for chunk in chunks:
            knowledge_point = KnowledgePoint(
                content=chunk,
                source_id=source_info.source_id,
                source_url=source_info.url,
                knowledge_type='general',
                domain=domain,
                credibility_score=source_info.credibility_score,
                extraction_timestamp=datetime.utcnow(),
                metadata={
                    'collection_id': collection_id,
                    'extraction_method': 'generic_parser'
                }
            )
            
            knowledge_points.append(knowledge_point)
        
        return knowledge_points

    def _split_content_into_chunks(self, content: str, max_chunk_size: int = 1000) -> List[str]:
        """Split content into manageable chunks for processing"""
        if len(content) <= max_chunk_size:
            return [content]
        
        chunks = []
        sentences = re.split(r'[.!?]+', content)
        
        current_chunk = ""
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if len(current_chunk) + len(sentence) + 1 > max_chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += (" " + sentence) if current_chunk else sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks

    def _classify_knowledge_type(self, content: str, domain: str, available_types: List[str]) -> str:
        """Classify knowledge type based on content patterns"""
        content_lower = content.lower()
        
        # Get patterns for this domain
        domain_patterns = self.extraction_patterns.get(domain, {})
        
        # Check patterns for each knowledge type
        for knowledge_type, patterns in domain_patterns.items():
            if knowledge_type in available_types:
                for pattern in patterns:
                    if re.search(pattern, content_lower, re.IGNORECASE):
                        return knowledge_type
        
        # Return first available type as default
        return available_types[0] if available_types else 'general'

    def _calculate_freshness_score(self, last_modified_header: Optional[str]) -> float:
        """Calculate freshness score from Last-Modified header"""
        if not last_modified_header:
            return 0.5  # Neutral score if no timestamp
        
        try:
            last_modified = datetime.strptime(last_modified_header, '%a, %d %b %Y %H:%M:%S %Z')
            return self._calculate_freshness_score_from_datetime(last_modified)
        except:
            return 0.5

    def _calculate_freshness_score_from_datetime(self, timestamp: datetime) -> float:
        """Calculate freshness score from datetime"""
        now = datetime.utcnow()
        age_days = (now - timestamp).total_seconds() / (24 * 3600)
        
        # Score decreases as content gets older
        if age_days <= 1:
            return 1.0
        elif age_days <= 7:
            return 0.9
        elif age_days <= 30:
            return 0.7
        elif age_days <= 90:
            return 0.5
        elif age_days <= 365:
            return 0.3
        else:
            return 0.1

    async def _analyze_content_changes(self, source_info: SourceInfo, new_content: str) -> Dict[str, Any]:
        """Analyze what changed in the content"""
        # This would implement more sophisticated change analysis
        # For now, return basic change information
        return {
            'change_type': 'content_updated',
            'content_size': len(new_content),
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'significant_changes': True  # Placeholder
        }

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on source monitor"""
        try:
            health_info = {
                'healthy': True,
                'sources_configured': len(self.source_configs),
                'source_status': {},
                'last_check': datetime.utcnow().isoformat()
            }
            
            # Test connectivity to a few sources
            test_sources = list(self.source_configs.keys())[:3]  # Test first 3 sources
            
            for source_id in test_sources:
                source_info = self.source_configs[source_id]
                
                try:
                    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                        async with session.head(source_info.url) as response:
                            health_info['source_status'][source_id] = {
                                'status': 'healthy' if response.status == 200 else 'warning',
                                'http_status': response.status,
                                'url': source_info.url
                            }
                except Exception as e:
                    health_info['source_status'][source_id] = {
                        'status': 'error',
                        'error': str(e),
                        'url': source_info.url
                    }
                    health_info['healthy'] = False
            
            return health_info
            
        except Exception as e:
            logger.error(f"Source monitor health check failed: {str(e)}")
            return {
                'healthy': False,
                'error': str(e),
                'last_check': datetime.utcnow().isoformat()
            }

# Example usage and testing
async def test_source_monitor():
    """Test source monitor functionality"""
    monitor = SourceMonitor()
    
    # Test health check
    health = await monitor.health_check()
    print(f"Health check: {health}")
    
    # Test change detection
    changes = await monitor.check_source_changes('react_docs')
    print(f"React docs changes: {changes}")
    
    # Test knowledge extraction
    knowledge = await monitor.extract_collection_knowledge(
        'react_patterns_comprehensive', 
        ['react_docs']
    )
    print(f"Extracted knowledge: {knowledge['point_count']} points")

if __name__ == "__main__":
    asyncio.run(test_source_monitor())