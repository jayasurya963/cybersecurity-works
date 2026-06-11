## Smart Wordlist Generator
A targeted, intelligent wordlist generator that crawls a website and builds a custom dictionary using real words, names, products, and terminology from the target. Perfect for security testing, password cracking, and reconnaissance.

**Important Notes** 
- Only use on websites you own or you have explicit permission to test.
- Be respectful with crawl rate to avoid getting blocked.
- Wordlist size is limited to few entries.

## Features
- **Intelligent Web Crawling**: Extracts words from page content, titles, links, etc.
- **Smart Mutations**: Generates variations (capitalization, numbers, symbols, basic leetspeak)
- **Domain-aware**: Stays within the same website
- **Customizable**: Adjustable crawl depth and delay
- **Ready to Use**: Outputs clean `.txt` wordlist compatible with Hydra, John, Hashcat, etc.

## Tech Stack
- Python
- BeautifulSoup4 (web scraping)
- Requests + fake-useragent (stealth crawling)
- Regular Expressions (word extraction)


**Create your -- 'python -m venv venv' -> Install the dependencies using 'pip'**

- Run as 'python wordlist_generator.py https://example.com --pages 30 --output company_wordlist.txt'
- Example Output -> company_wordlist.txt

