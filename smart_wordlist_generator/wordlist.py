import argparse
import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urlparse, urljoin
from fake_useragent import UserAgent
import os
from datetime import datetime

class SmartWordlistGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.session.headers.update({'User-Agent': self.ua.random})
        self.visited = set()
        self.words = set()

    def crawl(self, start_url, max_pages=30, delay=1.2):
        print(f"🚀 Crawling: {start_url} (max {max_pages} pages)")
        to_visit = [start_url]

        while to_visit and len(self.visited) < max_pages:
            url = to_visit.pop(0)
            if url in self.visited: continue

            try:
                print(f"   ↳ {url}")
                resp = self.session.get(url, timeout=12)
                resp.raise_for_status()

                self.visited.add(url)
                soup = BeautifulSoup(resp.text, 'lxml')

                for script in soup(["script", "style"]):
                    script.decompose()

                text = soup.get_text()
                found = re.findall(r'\b[a-zA-Z0-9@._-]{4,40}\b', text)
                for w in found:
                    if len(w) >= 4:
                        self.words.add(w.lower())

                # Find links
                for a in soup.find_all('a', href=True):
                    next_url = urljoin(url, a['href'])
                    if self.is_same_domain(start_url, next_url) and next_url not in self.visited:
                        to_visit.append(next_url)

                time.sleep(delay + random.uniform(0, 0.8))

            except Exception as e:
                print(f"   ⚠️ Error: {e}")

        print(f"✅ Crawl complete. {len(self.words)} unique words found.")

    def is_same_domain(self, base, check):
        return urlparse(base).netloc in urlparse(check).netloc

    def generate_mutations(self, min_length=6):
        print("🔧 Generating smart mutations...")
        mutations = set()

        for word in self.words:
            if len(word) < min_length: continue
            mutations.add(word)
            mutations.add(word.capitalize())
            mutations.add(word.upper())

            # Common patterns
            for suffix in ['123', '1234', '2024', '2025', '!', '@', '#', '$', 'admin']:
                mutations.add(word + suffix)
                mutations.add(word.capitalize() + suffix)

            # Basic leetspeak
            leet = word.replace('a','@').replace('e','3').replace('i','1').replace('o','0').replace('s','$')
            if leet != word:
                mutations.add(leet)

        return sorted(list(mutations), key=len)

    def save(self, filename):
        mutations = self.generate_mutations()
        with open(filename, "w", encoding="utf-8") as f:
            for word in mutations[:30000]:
                f.write(word + "\n")
        print(f"💾 Saved {len(mutations)} words → {filename}")

# ====================== CLI ======================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart Targeted Wordlist Generator")
    parser.add_argument("url", help="Target URL (e.g. https://example.com)")
    parser.add_argument("-p", "--pages", type=int, default=25, help="Max pages to crawl")
    parser.add_argument("-d", "--delay", type=float, default=1.2, help="Delay between requests")
    parser.add_argument("-o", "--output", default=None, help="Output filename")
    parser.add_argument("-m", "--min-length", type=int, default=6)

    args = parser.parse_args()

    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        args.output = f"wordlist_{urlparse(args.url).netloc}_{timestamp}.txt"

    generator = SmartWordlistGenerator()
    generator.crawl(args.url, max_pages=args.pages, delay=args.delay)
    generator.save(args.output)

    print("\n🎉 Wordlist ready for use with Hydra, John, Hashcat, etc.")
