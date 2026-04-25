import feedparser
import time
import re
import os
from config import FEEDS_FILE, FETCH_INTERVAL
from database import GUIDTracker
from notifier import post_to_discord

def get_feed_urls():
    if not os.path.exists(FEEDS_FILE):
        return []
    with open(FEEDS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def extract_course_name(url):
    # Regex to find the course code (e.g., IAED or CDI93610)
    match = re.search(r'/disciplinas/([^/]+)/', url)
    return match.group(1) if match else "IST News"

def main():
    print("Toaster IST Bot Started. Monitoring RSS feeds...")
    db = GUIDTracker()

    while True:
        urls = get_feed_urls()
        for url in urls:
            try:
                course_name = extract_course_name(url)
                feed = feedparser.parse(url)
                
                # reversed() so we post the oldest unread news first
                for entry in reversed(feed.entries):
                    guid = getattr(entry, 'guid', entry.link)
                    if db.is_new(guid):
                        post_to_discord(entry, course_name)
                        db.add(guid)
                        
            except Exception as e:
                print(f"Error processing {url}: {e}")
        
        print(f"Sweep complete. Sleeping for {FETCH_INTERVAL}s...")
        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    main()
