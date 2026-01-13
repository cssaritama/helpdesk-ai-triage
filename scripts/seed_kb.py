"""Seed the Knowledge Base with sample articles.

Usage:
  python scripts/seed_kb.py

Prerequisites:
  - Backend running locally (default: http://localhost:8000)
"""
import os
import requests

API = os.getenv("API_BASE_URL", "http://localhost:8000")

ARTICLES = [
  {
    "title": "Password Reset: Self-Service Steps",
    "body_markdown": (
      "# Password Reset\n\n"
      "If you cannot access your account, use the self-service password reset flow:\n\n"
      "1. Go to the sign-in page\n"
      "2. Click **Forgot password**\n"
      "3. Follow the email instructions\n\n"
      "If you do not receive an email within 5 minutes, check spam/junk folders."
    ),
    "tags": ["account", "password", "login"]
  },
  {
    "title": "Billing: Failed Payment Troubleshooting",
    "body_markdown": (
      "# Failed Payment\n\n"
      "Common causes:\n\n"
      "- Expired card\n"
      "- Insufficient funds\n"
      "- Bank declined\n\n"
      "Try a different payment method or contact your bank to allow the transaction."
    ),
    "tags": ["billing", "payments"]
  },
  {
    "title": "Technical: App Crash on Startup (Desktop)",
    "body_markdown": (
      "# App Crash on Startup\n\n"
      "Steps:\n\n"
      "1. Update to the latest version\n"
      "2. Clear local cache\n"
      "3. Reinstall if the crash persists\n\n"
      "Collect logs from Settings → Diagnostics and attach them to the ticket."
    ),
    "tags": ["technical", "crash", "desktop"]
  },
]

def main() -> None:
    for a in ARTICLES:
        r = requests.post(f"{API}/kb/articles", json=a, timeout=10)
        r.raise_for_status()
        print("Created:", r.json()["id"], "-", a["title"])

if __name__ == "__main__":
    main()
