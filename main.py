import requests
from bs4 import BeautifulSoup
import re

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

        # Try to fetch token (basic example, not Graph token)
        cookies = session.cookies.get_dict()
        print("[!] Session Cookies:", cookies)

        fb_dtsg_search = session.get("https://mbasic.facebook.com/composer/ocelot/async_loader/?publisher=feed", headers=headers)
        token_search = re.search(r'"accessToken":"(.*?)"', fb_dtsg_search.text)
        if token_search:
            access_token = token_search.group(1)
            print(f"[✓] Access Token Found:\n{access_token}")
        else:
            print("[✗] Couldn't find access token, session may require app password or checkpoint.")

    else:
        print("[✗] Login failed! Check credentials or checkpoint block.")

if __name__ == "__main__":
    email = input("[?] Enter Facebook Email: ")
    password = input("[?] Enter Facebook Password: ")
    login_facebook(email, password)
