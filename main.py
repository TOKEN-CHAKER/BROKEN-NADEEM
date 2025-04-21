import requests
import re
import time
import os
import sys

# === Logo Reveal Animation ===
def animated_logo():
    os.system('clear')
    print("""
    ███    ██  █████  ██████  ███████ ███████ ███    ███
    ████   ██ ██   ██ ██   ██ ██      ██      ████  ████
    ██ ██  ██ ███████ ██████  █████   █████   ██ ████ ██
    ██  ██ ██ ██   ██ ██      ██      ██      ██  ██  ██
    ██   ████ ██   ██ ██      ███████ ███████ ██      ██
    -----------------------------------------------
       [ Facebook Token Generator ] - Broken Nadeem
       [ Powered by: Aliya x Nadeem ]
    -----------------------------------------------
    """)

# === Loading Animation ===
def loading(msg):
    for i in range(3):
        sys.stdout.write(f"\r{msg}{'.' * i}   ")
        sys.stdout.flush()
        time.sleep(0.5)
    print("")

# === Token Generator from Cookie ===
def generate_token(cookie):
    headers = {
        'authority': 'business.facebook.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'cookie': cookie,
    }

    try:
        loading("[+] Generating token, please wait")
        response = requests.get('https://business.facebook.com/business_locations', headers=headers)
        token = re.search(r'"accessToken":"(EAA\w+)"', response.text)

        if token:
            access_token = token.group(1)
            print("\n[ Aliya x Nadeem ]")
            print("==========================================")
            print("   Your Token Successful:")
            print(f"\n   {access_token}")
            print("==========================================")
        else:
            print("\n[×] Invalid or expired cookie - Aliya x Nadeem")

    except Exception as e:
        print(f"[!] Error - Aliya x Nadeem: {str(e)}")

# === Main Program ===
if __name__ == '__main__':
    animated_logo()
    cookie_input = input("Paste your Facebook cookie:\n> ")
    generate_token(cookie_input)
