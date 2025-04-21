import requests
import time
import os
import random
import sys

def clear(): os.system("clear")

def slow(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def logo():
    clear()
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┃   BROKEN NADEEM - FB TOKEN TOOL    ┃")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")

user_agents = [
    "Mozilla/5.0 (Linux; Android 10; SM-A107F)",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 10)",
    "Mozilla/5.0 (Linux; Android 13; Realme C25)",
    "Mozilla/5.0 (Linux; Android 11; Vivo 1904)",
]

def try_login(email, password, ua):
    url = "https://b-api.facebook.com/method/auth.login"
    params = {
        "format": "json",
        "email": email,
        "password": password,
        "credentials_type": "password",
        "generate_session_cookies": 1,
        "error_detail_type": "button_with_disabled",
        "source": "device_based_login",
        "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
        "locale": "en_US",
        "method": "auth.login"
    }
    headers = {
        "User-Agent": ua,
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive"
    }
    try:
        r = requests.get(url, params=params, headers=headers)
        return r.json()
    except Exception as e:
        return {"error_msg": str(e)}

def main():
    logo()
    email = input("[+] Enter Facebook Email/Number: ")
    password = input("[+] Enter Facebook Password: ")

    attempt = 1
    while True:
        ua = random.choice(user_agents)
        print(f"\n[~] Attempt {attempt} | Logging in using: {ua}")
        response = try_login(email, password, ua)

        if "access_token" in response:
            token = response["access_token"]
            slow("\n[✓] Token Extracted Successfully!", 0.02)
            print(f"[>] Token: {token}")
            with open("fb_token.txt", "w") as f:
                f.write(token)
            print("[+] Saved to fb_token.txt")
            break

        elif "error_msg" in response and "www.facebook.com" in response["error_msg"]:
            print("[!] Checkpoint detected. Login approval required.")
            print("[~] Please approve login from your Facebook ID.")
            time.sleep(5)
        else:
            print(f"[✗] Login failed. Error: {response.get('error_msg', 'Unknown error')}")
            break

        attempt += 1

if __name__ == "__main__":
    main()
