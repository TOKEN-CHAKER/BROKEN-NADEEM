import requests
import re
import os
import time

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def banner():
    print("\033[1;95m")
    print("="*60)
    print("        BROKEN NADEEM | FB COOKIE TO TOKEN TOOL")
    print("="*60)
    print("\033[0m")

def extract_token(cookie):
    headers = {
        "Host": "business.facebook.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Referer": "https://business.facebook.com/"
    }

    print("\n\033[1;33m[*] Requesting Token from Facebook...\033[0m")

    try:
        response = requests.get("https://business.facebook.com/business_locations", headers=headers)

        if "accessToken" in response.text:
            token = re.search(r'"accessToken":"(EAA\w+)"', response.text).group(1)
            print(f"\n\033[1;32m[✓] Token Generated Successfully:\n{token}\033[0m\n")
            with open("fb_token.txt", "w") as file:
                file.write(token)
            print("\033[1;34m[+] Saved Token to fb_token.txt\033[0m\n")
        else:
            print("\033[1;31m[✗] Failed to Extract Token. Maybe Cookie is Invalid or Checkpoint Required.\033[0m\n")

    except Exception as e:
        print(f"\033[1;31m[✗] Error: {str(e)}\033[0m\n")

def main():
    clear()
    banner()
    print("\033[1;36m[!] Paste Your Full Facebook Cookie Below:\033[0m\n")
    cookie = input(">> ").strip()
    
    if not cookie:
        print("\033[1;31m[!] Cookie cannot be empty. Try again.\033[0m")
        return

    print("\n\033[1;33m[*] Extracting, Please Wait...\033[0m")
    time.sleep(1)
    extract_token(cookie)

if __name__ == "__main__":
    main()
