import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urlparse, urljoin
from fake_useragent import UserAgent
import os

class SmartWordlistGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.session.headers.update({'User-Agent': self.ua.random})
        self.visited = set()
        self.words = set()

    def crawl(self, start_url, max_pages=30, delay=1):
        """Crawl website and extract words"""
        print(f"🚀 Starting crawl on: {start_url}")
        
        to_visit = [start_url]
        
        while to_visit and len(self.visited) < max_pages:
            url = to_visit.pop(0)
            if url in self.visited:
                continue
                
            try:
                print(f"📄 Crawling: {url}")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                self.visited.add(url)
                
                # Extract text
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Remove script and style
                for script in soup(["script", "style"]):
                    script.decompose()
                
                text = soup.get_text()
                
                # Extract words (alphanumeric + some special chars)
                found_words = re.findall(r'\b[a-zA-Z0-9@._-]{3,30}\b', text)
                for word in found_words:
                    if len(word) >= 3:
                        self.words.add(word.lower())
                
                # Find more links
                for link in soup.find_all('a', href=True):
                    next_url = urljoin(url, link['href'])
                    if self.is_same_domain(start_url, next_url) and next_url not in self.visited:
                        to_visit.append(next_url)
                
                time.sleep(delay + random.uniform(0, 1))
                
            except Exception as e:
                print(f"⚠️ Error crawling {url}: {e}")
        
        print(f"✅ Crawl finished. Found {len(self.words)} unique words.")

    def is_same_domain(self, base_url, check_url):
        base_domain = urlparse(base_url).netloc
        check_domain = urlparse(check_url).netloc
        return base_domain in check_domain or check_domain in base_domain

    def generate_mutations(self):
        """Create common password variations"""
        print("🔧 Generating mutations...")
        base_words = list(self.words)
        mutations = set(base_words)
        
        common_suffixes = ['123', '1234', '2023', '2024', '2025', '!', '@', '#', '$']
        
        for word in base_words:
            mutations.add(word.capitalize())
            mutations.add(word.upper())
            
            for suffix in common_suffixes:
                mutations.add(word + suffix)
                mutations.add(word.capitalize() + suffix)
            
            # Leetspeak basics
            leet = word.replace('a', '@').replace('e', '3').replace('i', '1').replace('o', '0')
            if leet != word:
                mutations.add(leet)
        
        return sorted(list(mutations), key=len)

    def save_wordlist(self, filename="custom_wordlist.txt"):
        mutations = self.generate_mutations()
        with open(filename, "w", encoding="utf-8") as f:
            for word in mutations[:20000]:  # Limit size
                f.write(word + "\n")
        
        print(f"💾 Wordlist saved as '{filename}'")
        print(f"Total entries: {len(mutations)}")

# ============== MAIN ==============
if __name__ == "__main__":
    target = input("Enter target website URL (e.g. https://example.com): ").strip()
    if not target.startswith("http"):
        target = "https://" + target
    
    generator = SmartWordlistGenerator()
    generator.crawl(target, max_pages=25, delay=1.5)
    generator.save_wordlist()
    
    print("\n🎉 Done! Use this wordlist with tools like Hydra, Medusa, or John the Ripper.")