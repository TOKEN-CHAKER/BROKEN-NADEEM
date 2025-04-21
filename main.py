import requests, time, re, os
from bs4 import BeautifulSoup

def clear():
    os.system('clear')

def login_and_get_token(email, password):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-A107F Build/QP1A.190711.020)"
    }

    data = {
        "email": email,
        "pass": password
    }

    login_url = "https://mbasic.facebook.com/login.php"
    response = session.post(login_url, data=data, headers=headers)

    if "save-device" in response.url or "home.php" in response.url:
        print("[✓] Login Successful! Getting token...")
        token = extract_token(session)
        if token:
            print(f"\n[HU] Broken Nadeem Token Found: {token}")
            with open("token.txt", "w") as f:
                f.write(token)
        else:
            print("[X] Token not found!")
    elif "checkpoint" in response.url:
        print("[!] Checkpoint Detected. Waiting for approval...")
        while True:
            time.sleep(5)
            print("[HU] Please approval karo ID...")
            response = session.get("https://mbasic.facebook.com/home.php")
            if "save-device" in response.url or "home.php" in response.url:
                print("[✓] Approved! Extracting token...")
                token = extract_token(session)
                if token:
                    print(f"\n[HU] Broken Nadeem Token Found: {token}")
                    with open("token.txt", "w") as f:
                        f.write(token)
                else:
                    print("[X] Token not found!")
                break
    else:
        print("[X] Login failed. Wrong credentials or blocked ID.")

def extract_token(session):
    res = session.get("https://mbasic.facebook.com/composer/ocelot/async_loader/?publisher=feed")
    match = re.search(r'EAAA\w+', res.text)
    if match:
        return match.group(0)
    return None

def main():
    clear()
    print("""
██████╗ ██████╗  ██████╗ ██╗  ██╗███████╗███╗   ███╗
██╔══██╗██╔══██╗██╔════╝ ██║  ██║██╔════╝████╗ ████║
██████╔╝██████╔╝██║  ███╗███████║█████╗  ██╔████╔██║
██╔═══╝ ██╔═══╝ ██║   ██║██╔══██║██╔══╝  ██║╚██╔╝██║
██║     ██║     ╚██████╔╝██║  ██║███████╗██║ ╚═╝ ██║
╚═╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝
             [ Broken Nadeem - HU Version ]
""")
    email = input("[?] Gmail: ")
    password = input("[?] Password: ")
    login_and_get_token(email, password)

if __name__ == "__main__":
    main()
