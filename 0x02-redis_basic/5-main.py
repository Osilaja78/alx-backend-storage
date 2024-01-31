#!/usr/bin/env python3

from web import get_page

def main():
    # Test URLs
    urls = [
        "http://slowwly.robertomurray.co.uk/delay/1000/url/https://www.google.com",
        "http://slowwly.robertomurray.co.uk/delay/2000/url/https://www.python.org",
        "http://slowwly.robertomurray.co.uk/delay/3000/url/https://www.github.com"
    ]

    # Test the get_page function for each URL
    for url in urls:
        print(f"Fetching content from: {url}")
        content = get_page(url)
        print(f"Content length: {len(content)}")
        print()

if __name__ == "__main__":
    main()
