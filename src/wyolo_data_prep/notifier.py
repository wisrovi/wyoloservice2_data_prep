import requests
import os
import logging

class SlackNotifier:
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
        
    def send_alert(self, title: str, message: str, level: str = "info") -> bool:
        """
        Sends an alert to Slack.
        Levels: info, warning, error, success
        """
        if not self.webhook_url:
            logging.warning("Slack webhook URL not configured.")
            return False
            
        colors = {
            "info": "#3498db",
            "warning": "#f39c12",
            "error": "#e74c3c",
            "success": "#2ecc71"
        }
        
        payload = {
            "attachments": [
                {
                    "color": colors.get(level, "#3498db"),
                    "title": title,
                    "text": message
                }
            ]
        }
        
        try:
            resp = requests.post(self.webhook_url, json=payload, timeout=5)
            return resp.status_code == 200
        except Exception as e:
            logging.error(f"Failed to send Slack alert: {e}")
            return False
