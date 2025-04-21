import requests
import re
import os

def show_logo():
    os.system("clear")
    print("""
\033[1;32m╔══════════════════════════════════════╗
║         𝗕𝗿𝗼𝗸𝗲𝗻 𝗡𝗮𝗱𝗲𝗲𝗺 𝗧𝗼𝗸𝗲𝗻 𝗧𝗼𝗼𝗹         ║
╠══════════════════════════════════════╣
║  FB Cookie to Token | Instant Result ║
║     Status: EAAB/EAAG Token Ready    ║
╚══════════════════════════════════════╝\033[0m
""")

def extract_token(cookie):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile)",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": cookie,
    }

    try:
        res = requests.get("https://mbasic.facebook.com/settings/apps/tabbed/", headers=headers)
        token = re.search(r'EAA\w+', res.text)
        if token:
            token = token.group(0)
            verify = requests.get(f"https://graph.facebook.com/me?fields=id,name&access_token={token}").json()
            if 'name' in verify:
                print(f"\n\033[1;32m[✓] Valid Token Found:\033[0m {token}")
                print(f"\033[1;36m[•] Name:\033[0m {verify['name']}")
                print(f"\033[1;36m[•] ID:\033[0m {verify['id']}")
                with open("token.txt", "w") as f:
                    f.write(token)
                print("\033[1;32m[✓] Token saved to token.txt\033[0m")
                return True
            else:
                print("\033[1;31m[×] Token extracted but expired/invalid.\033[0m")
                return False
        elif "checkpoint" in res.text.lower():
            print("\033[1;33m[!] Checkpoint Detected! Approve Login First.\033[0m")
            return False
        else:
            print("\033[1;31m[×] Token not found. Try different cookie.\033[0m")
            return False
    except Exception as e:
        print(f"\033[1;31m[!] Error:\033[0m {str(e)}")
        return False

def main():
    show_logo()
    cookie = input("\033[1;36m[Input] Paste Facebook Cookie:\033[0m\n> ").strip()
    extract_token(cookie)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[1;31m[!] Interrupted by user. Exiting...\033[0m")
