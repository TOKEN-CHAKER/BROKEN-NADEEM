import requests
import sys
import os
import time
import random

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def slow(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def logo():
    clear()
    print("\n")
    print("██████╗░██████╗░░█████╗░███████╗██╗░░██╗███████╗███╗░░██╗")
    print("██╔══██╗██╔══██╗██╔══██╗██╔════╝██║░░██║██╔════╝████╗░██║")
    print("██║░░██║██████╦╝██║░░██║█████╗░░███████║█████╗░░██╔██╗██║")
    print("██║░░██║██╔══██╗██║░░██║██╔══╝░░██╔══██║██╔══╝░░██║╚████║")
    print("██████╔╝██████╦╝╚█████╔╝███████╗██║░░██║███████╗██║░╚███║")
    print("╚═════╝░╚═════╝░░╚════╝░╚══════╝╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝")
    print("        » FB TOKEN EXTRACTOR - BROKEN NADEEM STYLE «")
    print("=========================================================\n")

user_agents = [
    "Dalvik/2.1.0 (Linux; Android 10; Redmi Note 9 Pro)",
    "Mozilla/5.0 (Linux; Android 11; SM-M205F)",
    "Mozilla/5.0 (Linux; Android 12; Mi A3)",
    "Dalvik/2.1.0 (Linux; U; Android 9; Redmi 7A)"
]

def get_access_token(email, password, user_agent):
    url = "https://b-api.facebook.com/method/auth.login"
    params = {
        "format": "json",
        "email": email,
        "password": password,
        "credentials_type": "password",
        "generate_session_cookies": 1,
        "error_detail_type": "button_with_disabled",
        "source": "device_based_login",
        "meta_inf_fbmeta": "",
        "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
        "locale": "en_US",
        "client_country_code": "US",
        "method": "auth.login"
    }

    headers = {
        "User-Agent": user_agent,
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        return response.json()
    except Exception as e:
        return {"error_msg": f"Request failed: {str(e)}"}

def loading_bar():
    for i in range(20):
        sys.stdout.write("\r[~] Auto approval bypassing" + "." * (i % 4))
        sys.stdout.flush()
        time.sleep(0.1)
    print()

def main():
    logo()
    email = input("[?] Enter Facebook Email: ")
    password = input("[?] Enter Facebook Password: ")

    max_wait = 300
    start = time.time()
    attempt = 1

    while True:
        ua = random.choice(user_agents)
        print(f"\n[!] Attempt {attempt} using UA: {ua}")
        result = get_access_token(email, password, ua)

        if "access_token" in result:
            token = result["access_token"]
            slow(f"\n[✓] Token Extracted Successfully!\n[>] Token: {token}", 0.02)
            with open("fb_token.txt", "w") as f:
                f.write(token)
            print("[+] Token saved to fb_token.txt")
            break

        elif "error_msg" in result and "www.facebook.com" in result["error_msg"]:
            elapsed = time.time() - start
            if elapsed > max_wait:
                slow("\n[✗] Timed out waiting for approval. Try again later.", 0.04)
                break
            else:
                slow(f"[✗] Checkpoint Detected: {result['error_msg']}", 0.02)
                loading_bar()
                print("[~] Reattempting with modified headers...\n")
                time.sleep(5)
        else:
            slow(f"[✗] Login Failed: {result.get('error_msg', 'Unknown error')}", 0.04)
            break

        attempt += 1

if __name__ == "__main__":
    main()
