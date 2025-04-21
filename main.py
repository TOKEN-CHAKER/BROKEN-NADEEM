import requests
import re
import time
import os

def show_logo():
    os.system('clear')
    print("""
\033[1;32m╔══════════════════════════════════════╗
║         𝗕𝗿𝗼𝗸𝗲𝗻 𝗡𝗮𝗱𝗲𝗲𝗺 𝗧𝗼𝗸𝗲𝗻 𝗧𝗼𝗼𝗹         ║
╠══════════════════════════════════════╣
║  FB Token Extractor | Termux Ready   ║
║     Status: CHECKPOINT SAFE          ║
╚══════════════════════════════════════╝
\033[0m""")

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
        token_match = re.search(r"EAAG\w+", response.text)
        if token_match:
            token = token_match.group(0)
            print("\n\033[1;32m[✓] Successfully Token Extracted:\033[0m\n", token)

            # Check token validity
            info = requests.get(f"https://graph.facebook.com/me?fields=id,name&access_token={token}").json()
            if 'name' in info:
                print("\033[1;36m[•] Name:\033[0m", info['name'])
                print("\033[1;36m[•] ID:\033[0m", info['id'])

                with open("token.txt", "w") as f:
                    f.write(token)
                return True
            else:
                print("\033[1;31m[×] Token Invalid or Expired after extraction.\033[0m")
                return False

        elif "checkpoint" in response.text.lower():
            print("\033[1;33m[!] Checkpoint Detected! Please Approve Manually...\033[0m")
            return False
        else:
            print("\033[1;31m[×] Invalid Cookies or Token Not Found.\033[0m")
            return False
    except Exception as e:
        print("\033[1;31m[!] Error:\033[0m", str(e))
        return False

def main():
    show_logo()
    cookie = input("\n\033[1;36m[Input] Paste Your Facebook Cookies:\033[0m\n> ").strip()

    while True:
        success = extract_token_from_cookies(cookie)
        if success:
            print("\033[1;32m[✓] Token saved in token.txt\033[0m")
            break
        else:
            print("\033[1;34m[~] Retrying in 5 seconds...\033[0m")
            time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[1;31m[!] Interrupted by user. Exiting...\033[0m")
