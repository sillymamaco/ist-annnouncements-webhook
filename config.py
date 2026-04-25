import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1497240161690325124/hHnw9S_kMNQSaLVttrdOcecNbMyAIuIhuro7yEXpVh3g2C0ilQhX7rcUZlx5T8rXhHcH"
DB_FILE = "/opt/istbot/ist-bot/seen_guids.txt"
FEEDS_FILE = "/opt/istbot/ist-bot/feeds.txt"
FETCH_INTERVAL = 300  # 5 minutes
IST_BLUE = 3447003

# Ensure the directory exists
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

# Mapping of course identifier (from URL) to Discord Role ID
COURSE_ROLES = {
    "CDI93610": "1497620447724834856",
    "EMD3610":  "1497620833445871616",
    "IAC23610": "1497620653950373938",
    "IAED23610":"1497620619406348409",
    "Fis33610": "1497620685835473047",
    "MO10":     "1497620780325015782",
    "CDI53610": "1497621239512957110",
    "Alge10":   "1497620750021169394",
    "noticias": "123456789012345678",
    "PEstatisticad103610": "1497620555225104474"
    }
