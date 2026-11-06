"""Slack notification client for reporting data preparation events and alerts."""

import logging
import os
from typing import Optional
import requests


class SlackNotifier:
    """Dispatches color-coded event notifications and pipeline alerts to Slack."""

    def __init__(self, webhook_url: Optional[str] = None) -> None:
        """Initialize SlackNotifier with optional custom webhook endpoint.

        Args:
            webhook_url (Optional[str]): Incoming webhook URL. Defaults to SLACK_WEBHOOK_URL env var.
        """
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")

    def send_alert(self, title: str, message: str, level: str = "info") -> bool:
        """Send formatted webhook notification message to Slack channel.

        Args:
            title (str): Header title for the alert.
            message (str): Body text describing the alert details.
            level (str): Alert severity level ('info', 'warning', 'error', 'success').

        Returns:
            bool: True if alert payload was accepted with status 200, False otherwise.
        """
        if not self.webhook_url:
            logging.warning("Slack webhook URL not configured.")
            return False

        colors = {
            "info": "#3498db",
            "warning": "#f39c12",
            "error": "#e74c3c",
            "success": "#2ecc71",
        }

        payload = {
            "attachments": [
                {
                    "color": colors.get(level, "#3498db"),
                    "title": title,
                    "text": message,
                }
            ]
        }

        try:
            resp = requests.post(self.webhook_url, json=payload, timeout=5)
            return resp.status_code == 200
        except Exception as e:
            logging.error(f"Failed to send Slack alert: {e}")
            return False
