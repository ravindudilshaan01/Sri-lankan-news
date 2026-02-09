import requests
from bs4 import BeautifulSoup

url = 'https://www.dailymirror.lk/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print(f"Fetching {url}...")
try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Test original selectors
        selectors = ['h3.title a', 'h2.entry-title a']
        print(f"\nTesting selectors: {selectors}")
        
        total_found = 0
        for selector in selectors:
            elements = soup.select(selector)
            count = len(elements)
            print(f"Selector '{selector}': Found {count} elements")
            total_found += count
            
            if count > 0:
                print(f"Sample text: {elements[0].get_text(strip=True)}")
        
        if total_found == 0:
            print("\nOriginal selectors failed. Analyzing page structure...")
            h4_tags = soup.find_all('h4')
            print(f"Total H4 tags: {len(h4_tags)}")
            
            found_with_link = 0
            for tag in h4_tags:
                link = tag.find('a')
                if link:
                    print("\n--- Found Headline Candidate ---")
                    print(f"Tag: h4")
                    print(f"Classes: {tag.get('class')}")
                    print(f"Link text: {link.get_text(strip=True)}")
                    print(f"Link href: {link.get('href')}")
                    print(f"Parent classes: {tag.find_parent().get('class')}")
                    found_with_link += 1
                    if found_with_link >= 3:
                        break


                
    else:
        print("Failed to fetch page")

except Exception as e:
    print(f"Error: {e}")
