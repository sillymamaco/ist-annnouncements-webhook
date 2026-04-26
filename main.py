import feedparser
import time
import re
from config import RSS_URLS, FETCH_INTERVAL
from database import GUIDTracker
from notifier import post_to_discord

def extract_course_name(url):
    if '/disciplinas/' in url:
        match = re.search(r'/disciplinas/([^/]+)/', url)
        return match.group(1) if match else "IST News"
    return "noticias"

def main():
    print("Toaster IST Bot Started. Monitoring RSS feeds...")
    db = GUIDTracker()

    while True:
        all_new_entries = []

        for url in RSS_URLS:
            try:
                course_abbr = extract_course_name(url)
                feed = feedparser.parse(url)
                
                for entry in feed.entries:
                    guid = getattr(entry, 'guid', entry.link)
                    if db.is_new(guid):
                        ts = entry.get('published_parsed', time.gmtime())
                        all_new_entries.append((ts, entry, course_abbr))
            except Exception as e:
                print(f"Error checking {url}: {e}")

        all_new_entries.sort(key=lambda x: x[0])

        for ts, entry, course_abbr in all_new_entries:
            post_to_discord(entry, course_abbr)
            db.add(getattr(entry, 'guid', entry.link))

        print(f"Sweep complete. Sleeping for {FETCH_INTERVAL}s...")
        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    main()
