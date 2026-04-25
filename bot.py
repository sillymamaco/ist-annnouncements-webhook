import feedparser
import requests
import time
import os

# ==========================================
# CONFIGURATION
# ==========================================
RSS_URLS = [
    "https://fenix.tecnico.ulisboa.pt/noticias/rss",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/CDI93610/2025-2026/2-semestre/rss/announcement",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/EMD3610/2025-2026/2-semestre/rss/announcement",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/IAC23610/2025-2026/2-semestre/rss/announcement",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/IAED23610/2025-2026/2-semestre/rss/announcement",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/Fis33610/2025-2026/2-semestre/rss/announcement",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/MO10/2025-2026/2-semestre/rss/announcement",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/CDI53610/2025-2026/2-semestre/rss/announcement",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/Alge10/2025-2026/2-semestre/rss/announcement"
]

WEBHOOK_URL = "https://discord.com/api/webhooks/1497240161690325124/hHnw9S_kMNQSaLVttrdOcecNbMyAIuIhuro7yEXpVh3g2C0ilQhX7rcUZlx5T8rXhHcH"
DB_FILE = "/opt/istbot/seen_guids.txt"

# ==========================================
# LOGIC
# ==========================================

def get_seen_guids():
    """Reads the database of already-posted announcement IDs."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def add_seen_guid(guid):
    """Saves a new announcement ID to the database."""
    with open(DB_FILE, "a") as f:
        f.write(guid + "\n")

def post_to_discord(entry, course_name):
    """Sends a formatted embed to the Discord Webhook."""
    payload = {
        "embeds": [{
            "title": f"[{course_name}] {entry.title}",
            "url": entry.link,
            "description": entry.get("summary", "No description available.")[:300] + "...",
            "color": 3447003, # IST Blue
            "footer": {"text": "Torradeira da Cave | CMTV"}
        }]
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Error posting to Discord: {e}")

def main():
    print("Toaster IST Bot Started. Monitoring RSS feeds...")
    seen_guids = get_seen_guids()
    
    while True:
        for url in RSS_URLS:
            try:
                # Extract course name from URL for better Discord titles
                # E.g., /disciplinas/IAED/ -> IAED
                parts = url.split('/')
                course_name = parts[parts.index('disciplinas') + 1] if 'disciplinas' in parts else "IST News"
                
                feed = feedparser.parse(url)
                
                # Check entries from newest to oldest
                for entry in reversed(feed.entries):
                    if entry.guid not in seen_guids:
                        post_to_discord(entry, course_name)
                        add_seen_guid(entry.guid)
                        seen_guids.add(entry.guid)
                        time.sleep(2) # Avoid Discord rate limits
                        
            except Exception as e:
                print(f"Error parsing {url}: {e}")
        
        # Wait 5 minutes before the next full sweep
        time.sleep(300)

if __name__ == "__main__":
    main()
