import os
import requests
from dotenv import load_dotenv

# Load updated .env
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

def test_github():
    token = os.getenv("GITHUB_TOKEN")
    print(f"--- Testing GitHub PAT ---")
    if not token:
        print("FAIL: GITHUB_TOKEN not found in .env")
        return
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://api.github.com/user", headers=headers)
    if response.status_code == 200:
        print(f"SUCCESS: Authenticated as {response.json().get('login')}")
    else:
        print(f"FAIL: GitHub returned {response.status_code} - {response.text}")

def test_telegram():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    print(f"\n--- Testing Telegram ---")
    if not token:
        print("FAIL: TELEGRAM_BOT_TOKEN not found in .env")
        return
    url = f"https://api.telegram.org/bot{token}/getMe"
    response = requests.get(url)
    if response.status_code == 200:
        bot_info = response.json().get("result")
        print(f"SUCCESS: Bot Name: {bot_info.get('first_name')} (@{bot_info.get('username')})")
    else:
        print(f"FAIL: Telegram returned {response.status_code} - {response.text}")

def test_slack():
    token = os.getenv("SLACK_BOT_TOKEN")
    print(f"\n--- Testing Slack Bot Token ---")
    if not token:
        print("FAIL: SLACK_BOT_TOKEN not found in .env")
        return
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post("https://slack.com/api/auth.test", headers=headers)
    data = response.json()
    if data.get("ok"):
        print(f"SUCCESS: Slack Bot Authenticated as: {data.get('user')} in workspace {data.get('team')}")
    else:
        print(f"FAIL: Slack auth.test failed: {data.get('error')}")

if __name__ == "__main__":
    test_github()
    test_telegram()
    test_slack()
