import requests
from bs4 import BeautifulSoup

def analyze_page(url, name):
    print("\n" + "="*70)
    print(f"Analyzing: {name}")
    print("="*70)
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all links with meaningful text
        all_links = soup.find_all('a', href=True)
        
        print(f"\nTotal links found: {len(all_links)}")
        print("\nLinks with long text (potential headlines):")
        
        count = 0
        for link in all_links:
            text = link.get_text(strip=True)
            href = link.get('href', '')
            
            # Filter for headline-like links
            if text and len(text) > 30 and len(text) < 200:
                # Check if it looks like a news article URL
                if 'news' in href.lower() or 'article' in href.lower() or len(href) > 20:
                    count += 1
                    if count <= 10:
                        print(f"\n{count}. Text: {text[:80]}")
                        print(f"   URL: {href[:80]}")
                        print(f"   Parent tag: {link.parent.name}")
                        print(f"   Parent class: {link.parent.get('class', [])}")
        
        print(f"\n\nTotal potential headlines found: {count}")
        
        # Try to find common patterns
        if count == 0:
            print("\nLooking for ANY links with text > 20 chars...")
            for i, link in enumerate(all_links[:20]):
                text = link.get_text(strip=True)
                if text and len(text) > 20:
                    print(f"\n{i+1}. {text[:60]}")
                    print(f"   href: {link.get('href', '')[:60]}")
                    print(f"   classes: {link.get('class', [])}")
                    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


# Test each site
analyze_page('https://www.adaderana.lk/news.php', 'Ada Derana')
analyze_page('https://www.newsfirst.lk/', 'News First')
analyze_page('https://colombogazette.com/', 'Colombo Gazette')
