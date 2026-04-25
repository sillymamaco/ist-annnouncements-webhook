import requests
import time
from config import WEBHOOK_URL, IST_BLUE, COURSE_ROLES

def post_to_discord(entry, course_name):
    # Retrieve the role ID from config; default to no ping if not found
    role_id = COURSE_ROLES.get(course_name)
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
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
        time.sleep(1) 
    except Exception as e:
        print(f"Error posting to Discord: {e}")
