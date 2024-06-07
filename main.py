import os
import requests
import json
import logging
from datetime import datetime, timedelta
import time
from notification import send_notification

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("torrent_search.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Load configuration from file
config = {
    "api_url": os.getenv("API_URL"),
    "api_key": os.getenv("API_KEY"),
    "mode": os.getenv("MODE", "adult"),
    "page_number": int(os.getenv("PAGE_NUMBER", 1)),
    "page_size": int(os.getenv("PAGE_SIZE", 25)),
    "check_interval": int(os.getenv("CHECK_INTERVAL", 3600)),
    "auth_username": os.getenv("AUTH_USERNAME"),
    "auth_password": os.getenv("AUTH_PASSWORD"),
    "notification_url": os.getenv("NOTIFICATION_URL"),
    "notification_topic": os.getenv("NOTIFICATION_TOPIC"),
    "notification_title": os.getenv("NOTIFICATION_TITLE"),
    "notification_priority": int(os.getenv("NOTIFICATION_PRIORITY", 3)),
    "notification_actions": json.loads(os.getenv("NOTIFICATION_ACTIONS", "[]"))
}

# API request URL and headers
url = config["api_url"]
headers = {
    "Content-Type": "application/json",
    "x-api-key": config["api_key"]
}

# Request payload
payload = {
    "mode": config["mode"],
    "pageNumber": config["page_number"],
    "pageSize": config["page_size"]
}

# Notification service authentication
auth = requests.auth.HTTPBasicAuth(config["auth_username"], config["auth_password"])


# Store notified items status
notified_items = {}

def fetch_data():
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses
        logger.info("Data fetched successfully")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None

def check_and_notify(data):
    now = datetime.now()
    items = data.get("data", {}).get("data", [])
    for item in items:
        try:
            logger.info(f"Processing item: {item}")  # Log each item being processed
            descr = item.get("smallDescr", "")
            status = item.get("status", {})
            promotion_rule = status.get("promotionRule", {})
            discount = promotion_rule.get("discount", "")
            end_time_str = promotion_rule.get("endTime", "")
            
            if descr.startswith("活動置頂") and discount == "FREE":
                if not end_time_str:
                    logger.warning(f"End time is missing for item {item['id']}")
                    continue
                
                end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
                remaining_days = (end_time - now).days
                item_id = item["id"]

                if remaining_days >= 7:
                    if item_id not in notified_items:
                        message = f"Notify: {descr}, End Time: {end_time_str}, Remaining Days: {remaining_days}"
                        logger.info(message)
                        send_notification(
                            url=config["notification_url"],
                            auth=auth,
                            topic=config["notification_topic"],
                            message=message,
                            title=config["notification_title"],
                            tags=["green_circle", "bust_in_silhouette"],
                            priority=config["notification_priority"],
                            actions=config["notification_actions"]
                        )
                        notified_items[item_id] = True
                elif item_id in notified_items:
                    logger.info(f"Cancel Notification: {descr}, End Time: {end_time_str}, Remaining Days: {remaining_days}")
                    notified_items.pop(item_id, None)
        except KeyError as e:
            logger.error(f"KeyError processing item {item}: Missing key {e}")
        except ValueError as e:
            logger.error(f"ValueError processing item {item}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error processing item {item}: {e}")

# Scheduled task to run periodically
def scheduled_task():
    while True:
        try:
            data = fetch_data()
            if data and data.get("message") == "SUCCESS":
                check_and_notify(data)
        except Exception as e:
            logger.error(f"Error in scheduled task: {e}")
        time.sleep(config["check_interval"])

if __name__ == "__main__":
    logger.info("Program started")
    try:
        scheduled_task()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
