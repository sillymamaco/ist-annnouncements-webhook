import requests
import time
from config import COURSES, LEIC_WEBHOOK, IST_BLUE

def post_to_discord(entry, course_name):
    course_data = COURSES.get(course_name, {"role": None, "webhooks": [LEIC_WEBHOOK]})
    
    webhooks = course_data.get("webhooks", [LEIC_WEBHOOK])
    role_id = course_data.get("role")
    
    content = f"<@&{role_id}>" if role_id else ""
    message_text = f"🚨 **Acordem, dropou anúncio de {course_name}** {content}:"

    payload = {
        "content": message_text,
        "embeds": [{
            "title": entry.title,
            "url": entry.link,
            "description": entry.get("summary", "No description available.")[:300] + "...",
            "color": IST_BLUE,
            "footer": {"text": "Torradeira da Cave | CMTV"}
        }]
    }
    
    for url in webhooks:
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            time.sleep(0.5) 
        except Exception as e:
            print(f"Error posting to {url}: {e}")
