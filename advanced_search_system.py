"""
Advanced Search and Scraping System for Veterans India AI Assistant
Combines web scraping, search, and LLM processing for comprehensive responses
"""

import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from urllib.parse import urljoin, urlparse
import re
from typing import List, Dict, Optional
import json
from datetime import datetime
import time
from googlesearch import search as google_search
import newspaper
from readability import Document
import trafilatura
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedSearchSystem:
    """
    Advanced web search and scraping system that:
    1. Searches for relevant URLs using Google/Bing
    2. Scrapes content from multiple sources
    3. Extracts and cleans text
    4. Processes with LLM for final response
    """
    
    def __init__(self, llm_config=None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200
        )
        self.llm_config = llm_config
        
    async def search_and_scrape(self, query: str, max_sites: int = 10, max_content_length: int = 50000) -> Dict:
        """
        Main function to search for query and scrape relevant content
        
        Args:
            query: Search query
            max_sites: Maximum number of sites to scrape
            max_content_length: Maximum content length per site
            
        Returns:
            Dict with scraped content and metadata
        """
        logger.info(f"Starting search for: {query}")
        
        # Step 1: Get search results
        urls = await self.get_search_urls(query, max_sites)
        logger.info(f"Found {len(urls)} URLs to scrape")
        
        # Step 2: Scrape content from URLs
        scraped_data = await self.scrape_multiple_urls(urls, max_content_length)
        
        # Step 3: Process and filter content
        processed_data = self.process_scraped_content(scraped_data, query)
        
        return {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'sources_count': len(processed_data['sources']),
            'total_content_length': sum(len(source['content']) for source in processed_data['sources']),
            'processed_content': processed_data
        }
    
    async def get_search_urls(self, query: str, max_results: int = 10) -> List[str]:
        """Get URLs from Google search"""
        try:
            # Use googlesearch-python library
            urls = []
            for url in google_search(query, num_results=max_results, sleep_interval=1):
                urls.append(url)
                if len(urls) >= max_results:
                    break
            return urls
        except Exception as e:
            logger.error(f"Error in Google search: {e}")
            # Fallback to DuckDuckGo or manual URL list
            return self.fallback_search_urls(query)
    
    def fallback_search_urls(self, query: str) -> List[str]:
        """Fallback search method when primary search fails"""
        # You can customize this with specific domains relevant to your use case
        base_urls = [
            f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
            f"https://www.britannica.com/search?query={query}",
            f"https://stackoverflow.com/search?q={query}",
        ]
        return base_urls[:5]  # Return first 5 as fallback
    
    async def scrape_multiple_urls(self, urls: List[str], max_content_length: int) -> List[Dict]:
        """Scrape content from multiple URLs concurrently"""
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': self.session.headers['User-Agent']}
        ) as session:
            tasks = [self.scrape_single_url(session, url, max_content_length) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
        # Filter out failed scrapes
        successful_scrapes = [result for result in results if isinstance(result, dict)]
        logger.info(f"Successfully scraped {len(successful_scrapes)} out of {len(urls)} URLs")
        
        return successful_scrapes
    
    async def scrape_single_url(self, session: aiohttp.ClientSession, url: str, max_length: int) -> Dict:
        """Scrape content from a single URL"""
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    content = self.extract_content(html, url)
                    
                    if content and len(content) > 100:  # Minimum content threshold
                        return {
                            'url': url,
                            'title': self.extract_title(html),
                            'content': content[:max_length],
                            'timestamp': datetime.now().isoformat(),
                            'status': 'success'
                        }
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            
        return {'url': url, 'status': 'failed', 'error': str(e)}
    
    def extract_content(self, html: str, url: str) -> str:
        """Extract clean text content using multiple methods"""
        # Method 1: Try trafilatura (best for article content)
        try:
            content = trafilatura.extract(html)
            if content and len(content) > 200:
                return content
        except:
            pass
        
        # Method 2: Try newspaper3k
        try:
            from newspaper import Article
            article = Article(url)
            article.set_html(html)
            article.parse()
            if article.text and len(article.text) > 200:
                return article.text
        except:
            pass
        
        # Method 3: Try readability
        try:
            doc = Document(html)
            soup = BeautifulSoup(doc.summary(), 'html.parser')
            content = soup.get_text(strip=True, separator=' ')
            if content and len(content) > 200:
                return content
        except:
            pass
        
        # Method 4: Basic BeautifulSoup extraction
        return self.basic_content_extraction(html)
    
    def basic_content_extraction(self, html: str) -> str:
        """Basic content extraction using BeautifulSoup"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
        
        # Try to find main content areas
        content_selectors = [
            'article', '[role="main"]', '.content', '#content', 
            '.post', '.entry', '.article-body', 'main'
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                text = content_elem.get_text(strip=True, separator=' ')
                if len(text) > 200:
                    return text
        
        # Fallback to body content
        body = soup.find('body')
        if body:
            return body.get_text(strip=True, separator=' ')
        
        return soup.get_text(strip=True, separator=' ')
    
    def extract_title(self, html: str) -> str:
        """Extract page title"""
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        
        # Try h1 as fallback
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text(strip=True)
        
        return "No title found"
    
    def process_scraped_content(self, scraped_data: List[Dict], query: str) -> Dict:
        """Process and filter scraped content"""
        sources = []
        all_content = ""
        
        for data in scraped_data:
            if data.get('status') == 'success' and data.get('content'):
                # Filter content relevance (basic keyword matching)
                content = data['content']
                if self.is_content_relevant(content, query):
                    sources.append({
                        'url': data['url'],
                        'title': data.get('title', 'Unknown Title'),
                        'content': content,
                        'relevance_score': self.calculate_relevance_score(content, query)
                    })
                    all_content += f"\n\n--- Source: {data['title']} ---\n{content}"
        
        # Sort by relevance
        sources.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return {
            'sources': sources,
            'combined_content': all_content,
            'summary_needed': len(all_content) > 10000  # Flag for LLM processing
        }
    
    def is_content_relevant(self, content: str, query: str) -> bool:
        """Basic relevance check"""
        query_words = query.lower().split()
        content_lower = content.lower()
        
        # Check if at least 30% of query words appear in content
        matches = sum(1 for word in query_words if word in content_lower)
        return matches >= len(query_words) * 0.3
    
    def calculate_relevance_score(self, content: str, query: str) -> float:
        """Calculate relevance score for content"""
        query_words = query.lower().split()
        content_lower = content.lower()
        
        score = 0
        for word in query_words:
            count = content_lower.count(word)
            score += count
        
        # Normalize by content length
        return score / max(len(content.split()), 1)
    
    async def generate_llm_response(self, processed_data: Dict, query: str) -> str:
        """Generate final response using LLM"""
        if not self.llm_config:
            return self.generate_basic_summary(processed_data, query)
        
        try:
            # Try to import and use LLM config
            try:
                from llm_config import LLMManager, get_llm_manager
                llm_manager = get_llm_manager()
                llm = llm_manager.load_model("llama3.2:1b")
            except:
                # Fallback to direct ChatOllama
                from langchain_ollama import ChatOllama
                llm = ChatOllama(model="llama3.2:1b", temperature=0.6)
            
            # Create prompt for LLM
            sources_info = ""
            for i, source in enumerate(processed_data['sources'][:5]):  # Top 5 sources
                sources_info += f"\n\nSource {i+1}: {source['title']}\nURL: {source['url']}\nContent: {source['content'][:1500]}..."
            
            prompt = f"""Based on the following web search results, provide a comprehensive and accurate answer to the query: "{query}"

Web Search Results:{sources_info}

Please provide a detailed, well-structured response that:
1. Directly answers the query
2. Synthesizes information from multiple sources
3. Includes relevant facts and details
4. Mentions key sources when appropriate
5. Is accurate and up-to-date

Response:"""

            response = llm.invoke(prompt)
            return response.content if hasattr(response, 'content') else str(response)
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return self.generate_basic_summary(processed_data, query)
    
    def generate_basic_summary(self, processed_data: Dict, query: str) -> str:
        """Generate basic summary without LLM"""
        if not processed_data['sources']:
            return f"I couldn't find relevant information about '{query}' from web sources."
        
        summary = f"Based on web search for '{query}', here's what I found:\n\n"
        
        for i, source in enumerate(processed_data['sources'][:3]):
            summary += f"{i+1}. From {source['title']}:\n"
            # Take first few sentences
            sentences = source['content'].split('.')[:3]
            summary += f"   {'. '.join(sentences)}.\n\n"
        
        summary += f"Sources: {len(processed_data['sources'])} websites analyzed"
        return summary

# Async wrapper function for easy integration
async def search_and_process(query: str, max_sites: int = 8) -> str:
    """
    Main function to search, scrape, and process web content
    
    Args:
        query: What to search for
        max_sites: How many sites to check
        
    Returns:
        Processed response string
    """
    search_system = AdvancedSearchSystem()
    
    # Get scraped data
    result = await search_system.search_and_scrape(query, max_sites)
    
    # Generate LLM response
    response = await search_system.generate_llm_response(
        result['processed_content'], 
        query
    )
    
    return response

# Synchronous wrapper for direct use
def search_web_and_answer(query: str, max_sites: int = 8) -> str:
    """Synchronous version of search_and_process"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(search_and_process(query, max_sites))

if __name__ == "__main__":
    # Test the system
    test_query = "latest developments in artificial intelligence 2025"
    print(f"Testing search for: {test_query}")
    
    result = search_web_and_answer(test_query, max_sites=5)
    print(f"\nResult:\n{result}")
