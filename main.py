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
║     Real EAAB/EAAC Token Extractor   ║
║       Status: VALID & CHECKED        ║
╚══════════════════════════════════════╝
\033[0m""")

def extract_token(cookie):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile)",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": cookie,
    }

    try:
        res = requests.get("https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed", headers=headers)
        token = re.search(r'"accessToken\\":\\"(EAA\w+)', res.text)
        if token:
            token = token.group(1)
            verify = requests.get(f"https://graph.facebook.com/me?fields=id,name&access_token={token}").json()
            if 'name' in verify:
                print(f"\033[1;32m[✓] Token:\033[0m {token}")
                print(f"\033[1;36m[•] Name:\033[0m {verify['name']}")
                print(f"\033[1;36m[•] ID:\033[0m {verify['id']}")
                with open("token.txt", "w") as f:
                    f.write(token)
                return True
            else:
                print("\033[1;31m[×] Token found but invalid/expired.\033[0m")
        elif "checkpoint" in res.text.lower():
            print("\033[1;33m[!] Checkpoint! Please approve manually...\033[0m")
        else:
            print("\033[1;31m[×] Token not found. Invalid Cookie.\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Error:\033[0m {str(e)}")
    return False

def main():
    show_logo()
    cookie = input("\033[1;36m[Input] Paste Facebook Cookie:\033[0m\n> ").strip()
    
    while True:
        if extract_token(cookie):
            print("\033[1;32m[✓] Token Saved to token.txt\033[0m")
            break
        else:
            print("\033[1;34m[~] Retrying in 5 seconds...\033[0m")
            time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[1;31m[!] Interrupted by user. Exiting...\033[0m")
