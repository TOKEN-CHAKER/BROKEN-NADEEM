import requests
import time
import os
import sys
import random

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def slow(text, delay=0.02):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def logo():
    clear()
    print("███╗░░░███╗░█████╗░██████╗░███████╗███╗░░██╗  ███╗░░██╗░█████╗░██████╗░███████╗███╗░░██╗")
    print("████╗░████║██╔══██╗██╔══██╗██╔════╝████╗░██║  ████╗░██║██╔══██╗██╔══██╗██╔════╝████╗░██║")
    print("██╔████╔██║███████║██████╦╝█████╗░░██╔██╗██║  ██╔██╗██║███████║██████╔╝█████╗░░██╔██╗██║")
    print("██║╚██╔╝██║██╔══██║██╔══██╗██╔══╝░░██║╚████║  ██║╚████║██╔══██║██╔═══╝░██╔══╝░░██║╚████║")
    print("██║░╚═╝░██║██║░░██║██████╦╝███████╗██║░╚███║  ██║░╚███║██║░░██║██║░░░░░███████╗██║░╚███║")
    print("╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═════╝░╚══════╝╚═╝░░╚══╝  ╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░░░░╚══════╝╚═╝░░╚══╝")
    print("                   » BROKEN NADEEM - TERMUX TOKEN TOOL «")
    print("=================================================================\n")

user_agents = [
    "Mozilla/5.0 (Linux; Android 10; SM-A107F Build/QP1A.190711.020)",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro)",
    "Dalvik/2.1.0 (Linux; Android 9; vivo 1901)",
    "Mozilla/5.0 (Linux; Android 12; Mi A3)"
]

def get_token(email, password, user_agent):
    url = "https://b-api.facebook.com/method/auth.login"
    params = {
        "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
        "format": "json",
        "sdk_version": "2",
        "email": email,
        "locale": "en_US",
        "password": password,
        "sdk": "android",
        "generate_session_cookies": "1",
        "sig": "3f555f99fb61fcd7aa0c44f58f522ef6"
    }

    headers = {
        "User-Agent": user_agent,
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive"
    }

    try:
        res = requests.get(url, params=params, headers=headers)
        return res.json()
    except Exception as e:
        return {"error_msg": str(e)}

def main():
    logo()
    email = input("[?] Gmail/Phone: ")
    password = input("[?] Password: ")

    ua = random.choice(user_agents)
    slow(f"\n[~] Trying to login using: {ua}", 0.02)
    result = get_token(email, password, ua)

    if "access_token" in result:
        token = result["access_token"]
        slow("\n[✓] Login Successful!", 0.02)
        print(f"[+] Access Token: {token}")
        with open("token.txt", "w") as f:
            f.write(token)
        print("[+] Token saved to token.txt")
    elif "error_msg" in result:
        if "www.facebook.com" in result["error_msg"]:
            slow("\n[!] Checkpoint Detected. Login requires manual approval.", 0.02)
        else:
            slow(f"[✗] Login failed: {result['error_msg']}", 0.02)
    else:
        slow("[✗] Unknown error occurred.", 0.02)

if __name__ == "__main__":
    main()
