import requests
import re
import time
import os
import sys

# === Logo Reveal Animation ===
def animated_logo():
    os.system('clear')
    logo_lines = [
        " ███    ██  █████  ██████  ███████ ███████ ███    ███ ",
        " ████   ██ ██   ██ ██   ██ ██      ██      ████  ████ ",
        " ██ ██  ██ ███████ ██████  █████   █████   ██ ████ ██ ",
        " ██  ██ ██ ██   ██ ██      ██      ██      ██  ██  ██ ",
        " ██   ████ ██   ██ ██      ███████ ███████ ██      ██ ",
    ]
    for line in logo_lines:
        print(line)
        time.sleep(0.1)
    print("\n  [ Facebook Token Generator ] - Broken Nadeem")
    print("  [ Powered by: Aliya x Nadeem ]\n")
    print("====================================================")

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
        'Host': 'business.facebook.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10)',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://business.facebook.com',
        'Connection': 'keep-alive',
        'Referer': 'https://business.facebook.com/',
        'Cookie': cookie,
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
