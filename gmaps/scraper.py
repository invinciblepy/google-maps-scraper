import json
import re
import requests
import csv
import os



class GoogleMapsScraper:
    def __init__(self, url: str):
        self.url = url
        if "google.com/maps/" not in url:
            print("Invalid URL")
            exit()

        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'downlink': '10',
            'priority': 'u=0, i',
            'rtt': '200',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version-list': '"Chromium";v="136.0.7103.93", "Google Chrome";v="136.0.7103.93", "Not.A/Brand";v="99.0.0.0"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        })

        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
        os.makedirs(self.output_dir, exist_ok=True)

        self.filename = self.url.split("google.com/maps/")[1].split("/")[1]
        self.output_file = os.path.join(self.output_dir, f"{self.filename}.csv")
        self.headers = ["name", "address", "attributes", "place_id", "rating", "reviews_count", "phone", "url"]
        self.locations = []
        print("""
                 GOOGLE MAPS SCRAPER
---------------------------------------------------
Author : invinciblepy
GitHub : https://github.com/invinciblepy
Site   : https://hashamx.com
---------------------------------------------------""")

    def scrape(self):
        response = self.session.get(self.url)
        pattern = r'window\.APP_INITIALIZATION_STATE\s*=\s*\[(.*?)\];'
        match = re.search(pattern, response.text)
        if not match:
            print("No Items found")
            return
            
        state_str = match.group(1)
        state = json.loads(f"[{state_str}]")
        events_arr = state[3][2].replace(")]}'\n", "")
        all_events = json.loads(events_arr)
        self.locations = [
            self.fetch_event_data(event[1])
            if isinstance(event[1], list)
            else None
            for event in all_events[64]
        ]
        self.write_to_csv(self.locations)
        
    def fetch_event_data(self, event):
        return {
            "name": event[11],
            "address": event[18] or event[39],
            "attributes": ', '.join(attr[0] for attr in event[76]),
            "place_id": event[89],
            "rating": event[4][7],
            "reviews_count": event[4][8],
            "phone": event[178][0][0] if isinstance(event[178], list) else None,
            "url": event[7][0] if isinstance(event[7], list) else None
        }
    
    def write_to_csv(self, locations):
        with open(self.output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)
            for location in locations:
                if location:
                    writer.writerow([location[header] for header in self.headers])

if __name__ == "__main__":
    scraper = GoogleMapsScraper("https://www.google.com/maps/search/Hotels+near+Ile-de-France/@48.6715055,1.7096918,9z/data=!3m1!4b1?entry=ttu&g_ep=EgoyMDI1MDUwNy4wIKXMDSoASAFQAw%3D%3D")
    scraper.scrape()






