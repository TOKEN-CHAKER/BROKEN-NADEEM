import requests
import sys
import os
import time

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def slow(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def logo():
    clear()
    print("\n")
    print("██████╗░██████╗░░█████╗░███████╗██╗░░██╗███████╗███╗░░██╗")
    print("██╔══██╗██╔══██╗██╔══██╗██╔════╝██║░░██║██╔════╝████╗░██║")
    print("██║░░██║██████╦╝██║░░██║█████╗░░███████║█████╗░░██╔██╗██║")
    print("██║░░██║██╔══██╗██║░░██║██╔══╝░░██╔══██║██╔══╝░░██║╚████║")
    print("██████╔╝██████╦╝╚█████╔╝███████╗██║░░██║███████╗██║░╚███║")
    print("╚═════╝░╚═════╝░░╚════╝░╚══════╝╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝")
    print("        » FB TOKEN EXTRACTOR - BROKEN NADEEM STYLE «")
    print("=========================================================\n")

def get_token(email, password):
    url = "https://b-api.facebook.com/method/auth.login"
    params = {
        "format": "json",
        "email": email,
        "password": password,
        "credentials_type": "password",
        "generate_session_cookies": 1,
        "error_detail_type": "button_with_disabled",
        "source": "device_based_login",
        "meta_inf_fbmeta": "",
        "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
        "locale": "en_US",
        "method": "auth.login"
    }
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 8 Build/QKQ1)",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        r = requests.get(url, params=params, headers=headers)
        return r.json()
    except Exception as e:
        return {"error_msg": f"Connection failed: {str(e)}"}

def main():
    logo()
    email = input("[?] Facebook Email: ")
    password = input("[?] Facebook Password: ")

    print("\n[!] Login try ho raha hai...")

    retry_count = 0
    while retry_count < 5:
        result = get_token(email, password)

        if "access_token" in result:
            token = result["access_token"]
            slow(f"\n[✓] Token mil gaya!\n[>] Token: {token}", 0.03)
            with open("fb_token.txt", "w") as f:
                f.write(token)
            print("[+] Token 'fb_token.txt' mein save ho gaya hai.")
            return

        elif "error_msg" in result:
            error = result["error_msg"]
            if "www.facebook.com" in error:
                slow("[!] Account pe checkpoint laga hua hai.", 0.04)
                slow("[~] Manual approval do. Script har 5 second mein check karega...", 0.04)
                while True:
                    time.sleep(5)
                    result = get_token(email, password)
                    if "access_token" in result:
                        token = result["access_token"]
                        slow(f"\n[✓] Approval ke baad token mil gaya!\n[>] Token: {token}", 0.03)
                        with open("fb_token.txt", "w") as f:
                            f.write(token)
                        print("[+] Token 'fb_token.txt' mein save ho gaya hai.")
                        return
            else:
                retry_count += 1
                slow(f"[✗] Login Failed: {error} (try: {retry_count})", 0.03)
                time.sleep(2)
        else:
            retry_count += 1
            slow(f"[✗] Unknown response mila. Retry kar rahe hain... ({retry_count})", 0.03)
            time.sleep(2)

    print("\n[✗] 5 baar try kar liya. Login nahi ho paaya. Check karo credentials ya Facebook restriction.")

if __name__ == "__main__":
    main()
