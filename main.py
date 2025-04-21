import requests
import re
import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print("\033[1;35m" + "=" * 60)
    print("     FB COOKIE TO TOKEN EXTRACTOR - BROKEN NADEEM STYLE")
    print("=" * 60 + "\033[0m")

def extract_token(cookie):
    headers = {
        "Host": "business.facebook.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Cookie": cookie
    }

    url = "https://business.facebook.com/business_locations"

    try:
        response = requests.get(url, headers=headers)

        if "accessToken" in response.text:
            token = re.search(r'"accessToken":"(EAA\w+)"', response.text).group(1)
            print(f"\033[1;32m[✓] Successfully Token Generated: {token}\033[0m")
            with open("fb_token.txt", "w") as f:
                f.write(f"Cookie: {cookie}\nToken: {token}")
            print("\033[1;34m[+] Token saved to fb_token.txt\033[0m")
        else:
            print("\033[1;31m[✗] Token not found! Cookie may be invalid or need checkpoint approval.\033[0m")
    except Exception as e:
        print(f"\033[1;31m[✗] Error: {str(e)}\033[0m")

def main():
    clear()
    banner()
    print("\033[1;36m[Input] Enter Your Facebook Cookie:\033[0m")
    cookie = input(">> ").strip()
    print("\n\033[1;33m[!] Extracting token, please wait...\033[0m\n")
    extract_token(cookie)

if __name__ == "__main__":
    main()
