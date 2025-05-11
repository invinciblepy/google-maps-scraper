import argparse
from gmaps.scraper import GoogleMapsScraper

def main():
    parser = argparse.ArgumentParser(description="Google Maps Scraper CLI")
    parser.add_argument('-u', '--url', required=True, help='URL of the website to scrape')
    args = parser.parse_args()
    scraper = GoogleMapsScraper(url=args.url)
    scraper.scrape()

if __name__ == "__main__":
    main()