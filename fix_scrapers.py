import requests
from bs4 import BeautifulSoup

def test_ada_derana():
    print("\n" + "="*60)
    print("Testing Ada Derana")
    print("="*60)
    url = 'https://www.adaderana.lk/news.php'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try different selectors
        selectors = [
            'h2 a',
            'div.news-story h2 a',
            'a[href*="news/"]',
            'div.card-body h2 a',
            'h3 a',
            '.news-title a'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            print(f"\nSelector: '{selector}' - Found: {len(elements)}")
            if elements and len(elements) > 0:
                for i, elem in enumerate(elements[:3], 1):
                    text = elem.get_text(strip=True)
                    href = elem.get('href', '')
                    if text and len(text) > 20:
                        print(f"  {i}. {text[:70]}")
                        print(f"     URL: {href[:50]}")
    except Exception as e:
        print(f"Error: {e}")


def test_news_first():
    print("\n" + "="*60)
    print("Testing News First")
    print("="*60)
    url = 'https://www.newsfirst.lk/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        selectors = [
            'h3.entry-title a',
            'h2.post-title a',
            'h2 a',
            'h3 a',
            'article h2 a',
            'article h3 a',
            '.post-title a'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            print(f"\nSelector: '{selector}' - Found: {len(elements)}")
            if elements and len(elements) > 0:
                for i, elem in enumerate(elements[:3], 1):
                    text = elem.get_text(strip=True)
                    href = elem.get('href', '')
                    if text and len(text) > 20:
                        print(f"  {i}. {text[:70]}")
                        print(f"     URL: {href[:50]}")
    except Exception as e:
        print(f"Error: {e}")


def test_colombo_gazette():
    print("\n" + "="*60)
    print("Testing Colombo Gazette")
    print("="*60)
    url = 'https://colombogazette.com/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        selectors = [
            'h2.entry-title a',
            'h3.entry-title a',
            'h2 a',
            'h3 a',
            'article h2 a',
            'article h3 a',
            '.entry-title a'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            print(f"\nSelector: '{selector}' - Found: {len(elements)}")
            if elements and len(elements) > 0:
                for i, elem in enumerate(elements[:3], 1):
                    text = elem.get_text(strip=True)
                    href = elem.get('href', '')
                    if text and len(text) > 20:
                        print(f"  {i}. {text[:70]}")
                        print(f"     URL: {href[:50]}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_ada_derana()
    test_news_first()
    test_colombo_gazette()
