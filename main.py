import requests, time, os

def logo():
    os.system("clear")
    print("""

██████╗ ██████╗  ██████╗ ██╗  ██╗███████╗███╗   ██╗    ██╗   ██╗
██╔══██╗██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║    ██║   ██║
██████╔╝██████╔╝██║   ██║█████╔╝ █████╗  ██╔██╗ ██║    ██║   ██║
██╔═══╝ ██╔══██╗██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║    ╚██╗ ██╔╝
██║     ██║  ██║╚██████╔╝██║  ██╗███████╗██║ ╚████║     ╚████╔╝ 
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝      ╚═══╝  
               => TOKEN EXTRACTOR BY BROKEN NADEEM [HU]

""")

def login(email, password):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-A107F Build/QP1A.190711.020)"
    }

    data = {
        "email": email,
        "pass": password,
        "login": "Log In"
    }

    while True:
        logo()
        print("[~] Trying to login using: Mozilla/5.0 (Android)...")
        response = session.post("https://mbasic.facebook.com/login", data=data, headers=headers)

        if "c_user" in session.cookies.get_dict():
            print("\n[✓] Login Success!")
            token = session.cookies.get_dict()
            token_str = f"c_user={token['c_user']};xs={token['xs']}"
            print(f"[✓] Token: {token_str}")
            open("hu_token.txt", "w").write(token_str)
            break

        elif "checkpoint" in session.cookies.get_dict():
            print("\n[!] Checkpoint Detected. Please approve it manually.")
            time.sleep(5)
            continue

        else:
            print("\n[X] Login failed. Wrong credentials or blocked ID.")
            break

if __name__ == "__main__":
    logo()
    email = input("Enter Facebook Gmail/Number: ")
    password = input("Enter Password: ")
    login(email, password)
