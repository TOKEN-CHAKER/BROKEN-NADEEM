import requests
import os
import re

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print("=" * 60)
    print("     FB COOKIE TO TOKEN EXTRACTOR - BROKEN NADEEM STYLE")
    print("=" * 60)

def extract_token(cookie):
    url = "https://business.facebook.com/business_locations"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Cookie': cookie,
    }

    try:
        # Sending the GET request with the cookie
        res = requests.get(url, headers=headers)

        # Debug: check the response content
        if res.status_code != 200:
            print(f"[✗] Error: Status code {res.status_code}")
            return None

        # Try to match the token in the response
        token_match = re.search(r'"accessToken":"(EAA\w+)"', res.text)
        if token_match:
            return token_match.group(1)
        else:
            print("[✗] Error: Token not found in the response.")
            return None
    except Exception as e:
        print(f"[✗] Error: {str(e)}")
        return None

def single_cookie_mode():
    cookie = input("\n[?] Paste your Facebook Cookie: ").strip()
    print("\n[!] Extracting token, please wait...")
    token = extract_token(cookie)
    if token:
        print(f"\n[✓] Token Extracted: {token}")
        with open("fb_token.txt", "w") as f:
            f.write(token)
        print("[+] Token saved to fb_token.txt")
    else:
        print("[✗] Failed to extract token. Make sure the cookie is valid and from Facebook business page.")

def file_cookie_mode():
    path = input("\n[?] Enter path to cookie file (e.g., cookies.txt): ").strip()
    if not os.path.exists(path):
        print("[✗] File not found.")
        return

    with open(path, "r") as f:
        cookies = f.readlines()

    for idx, cookie in enumerate(cookies, start=1):
        cookie = cookie.strip()
        print(f"\n[!] Trying cookie #{idx}...")
        token = extract_token(cookie)
        if token:
            print(f"[✓] Token Extracted: {token}")
            with open("fb_token.txt", "w") as f:
                f.write(token)
            print("[+] Token saved to fb_token.txt")
            return
        else:
            print("[✗] Failed. Trying next if available...")

    print("\n[✗] No valid tokens found in file.")

def main():
    clear()
    banner()
    print("[1] Enter Single Cookie")
    print("[2] Load Cookies from File")
    print("=" * 60)
    choice = input("[?] Choose Option (1 or 2): ").strip()

    if choice == "1":
        single_cookie_mode()
    elif choice == "2":
        file_cookie_mode()
    else:
        print("[✗] Invalid option selected.")

if __name__ == "__main__":
    main()
