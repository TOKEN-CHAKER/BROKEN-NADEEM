import requests
import sys
import os
import time

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

def get_access_token_from_cookie(cookie):
    url = "https://business.facebook.com/business_locations"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Cookie": cookie
    }

    try:
        response = requests.get(url, headers=headers)
        token = None
        if 'accessToken' in response.text:
            token = response.text.split('accessToken":"')[1].split('"')[0]
        
        if token:
            return token
        else:
            return None
    except Exception as e:
        return {"error_msg": f"Request failed: {str(e)}"}

def main():
    logo()
    cookie = input("[?] Paste your Facebook Cookie: ")

    max_wait = 300  # 5 minutes
    start = time.time()
    attempt = 1

    while True:
        print(f"\n[!] Attempt {attempt} - Trying to extract token...")
        token = get_access_token_from_cookie(cookie)

        if token:
            slow(f"\n[✓] Token Extracted Successfully!\n[>] Token: {token}", 0.03)
            with open("fb_token.txt", "w") as f:
                f.write(token)
            print("[+] Token saved to fb_token.txt")
            break
        else:
            elapsed = time.time() - start
            if elapsed > max_wait:
                slow("\n[✗] Timed out. Cookie may be invalid or expired.", 0.04)
                break
            else:
                slow("[✗] Failed to extract token. Retrying...", 0.02)
                slow("[~] Waiting 15 seconds before retrying...", 0.02)
                time.sleep(15)

        attempt += 1

if __name__ == "__main__":
    main()
