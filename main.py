import requests
from bs4 import BeautifulSoup
import re
import os
import time

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def banner():
    clear()
    print("\n")
    print("██████╗░██████╗░░█████╗░███████╗██╗░░██╗███████╗███╗░░██╗")
    print("██╔══██╗██╔══██╗██╔══██╗██╔════╝██║░░██║██╔════╝████╗░██║")
    print("██║░░██║██████╦╝██║░░██║█████╗░░███████║█████╗░░██╔██╗██║")
    print("██║░░██║██╔══██╗██║░░██║██╔══╝░░██╔══██║██╔══╝░░██║╚████║")
    print("██████╔╝██████╦╝╚█████╔╝███████╗██║░░██║███████╗██║░╚███║")
    print("╚═════╝░╚═════╝░░╚════╝░╚══════╝╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝")
    print("      » FB TOKEN EXTRACTOR - BROKEN NADEEM STYLE «")
    print("=========================================================\n")

def login_facebook(email, password):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36',
    }

    login_page = session.get("https://mbasic.facebook.com/login", headers=headers)
    soup = BeautifulSoup(login_page.text, 'html.parser')
    inputs = soup.find_all("input")

    form_data = {}
    for i in inputs:
        if i.get("name"):
            form_data[i.get("name")] = i.get("value", "")
    form_data['email'] = email
    form_data['pass'] = password

    login = session.post("https://mbasic.facebook.com/login", headers=headers, data=form_data)
    if "save-device" in login.text or "home.php" in login.url:
        print("[✓] Login Successful!")

        cookies = session.cookies.get_dict()
        print("[!] Session Cookies:")
        for k, v in cookies.items():
            print(f"  {k}: {v}")

        # Token attempt
        token_url = "https://mbasic.facebook.com/composer/ocelot/async_loader/?publisher=feed"
        response = session.get(token_url, headers=headers)
        token_search = re.search(r'"accessToken":"(.*?)"', response.text)

        if token_search:
            token = token_search.group(1)
            print(f"\n[✓] Access Token:\n{token}")
            with open("fb_token.txt", "w") as f:
                f.write(token)
            print("[+] Token saved to fb_token.txt")
        else:
            print("\n[✗] Access token not found. Maybe checkpoint or app password needed.")
    else:
        print("[✗] Login failed. Wrong credentials or checkpoint lock.")

def main():
    banner()
    email = input("[?] Enter Facebook Email: ")
    password = input("[?] Enter Facebook Password: ")
    print("\n[~] Trying to login...\n")
    login_facebook(email, password)

if __name__ == "__main__":
    main()
