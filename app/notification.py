import requests
import json
import logging

logger = logging.getLogger(__name__)

def send_notification(url, auth, topic, message, title, tags, priority, actions):
    data = {
        "topic": topic,
        "message": message,
        "title": title,
        "tags": tags,
        "priority": priority,
        "actions": actions
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, auth=auth, data=json.dumps(data), headers=headers)
    
    if response.status_code == 200:
        logger.info("Notification sent successfully")
    else:
        logger.error(f"Failed to send notification: {response.status_code} - {response.text}")
