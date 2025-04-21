import requests
import re
import time

def extract_token_from_cookies(cookie):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile)",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": cookie,
    }

    try:
        response = requests.get(
            "https://business.facebook.com/business_locations", headers=headers
        )
        access_token = re.search(r"EAAG\w+", response.text)
        if access_token:
            token = access_token.group(0)
            print("\n[✓] Successfully Token Generated:\n", token)
            with open("token.txt", "w") as f:
                f.write(token)
            return True
        elif "checkpoint" in response.text.lower():
            print("[!] Checkpoint detected! Please approve manually...")
            return False
        else:
            print("[×] Invalid Cookies or Token Not Found.")
            return False
    except Exception as e:
        print("[!] Error:", e)
        return False

def main():
    print("\n===============================")
    print("  Facebook Token Extractor v2 ")
    print("        By Broken Nadeem")
    print("===============================\n")
    cookie = input("[Input] Paste Your Facebook Cookies:\n> ").strip()

    while True:
        success = extract_token_from_cookies(cookie)
        if success:
            break
        else:
            print("[~] Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Exiting...")
