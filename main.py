import requests
import os

def show_logo():
    os.system("clear")
    print("""
\033[1;35m╔════════════════════════════════════╗
║     𝗕𝗿𝗼𝗸𝗲𝗻 𝗡𝗮𝗱𝗲𝗲𝗺 - 𝗧𝗼𝗸𝗲𝗻 𝗖𝗵𝗲𝗰𝗸𝗲𝗿       ║
╠════════════════════════════════════╣
║   FB Graph API | Validity Checker  ║
║        Status: LIVE & FAST         ║
╚════════════════════════════════════╝
\033[0m""")

def check_token(token):
    url = f"https://graph.facebook.com/me?fields=id,name&access_token={token}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("\n\033[1;32m[✓] Valid Token Detected!\033[0m")
            print("\033[1;36m[•] Name:\033[0m", data.get("name"))
            print("\033[1;36m[•] ID:\033[0m", data.get("id"))
        else:
            print("\n\033[1;31m[×] Invalid or Expired Token!\033[0m")
            print("Response:", response.text)
    except Exception as e:
        print("\033[1;31m[!] Error:\033[0m", str(e))

def main():
    show_logo()
    token = input("\n\033[1;33m[Input] Paste Your Access Token:\033[0m\n> ").strip()
    check_token(token)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[1;31m[!] Interrupted by user. Exiting...\033[0m")
