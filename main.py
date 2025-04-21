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

def get_access_token(email, password):
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
        "client_country_code": "US",
        "method": "auth.login"
    }

    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; Android 10; Redmi Note 9 Pro Build/QKQ1.191215.002)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        return response.json()
    except Exception as e:
        return {"error_msg": f"Request failed: {str(e)}"}

def main():
    logo()
    email = input("[?] Enter Facebook Email: ")
    password = input("[?] Enter Facebook Password: ")

    max_wait = 600  # Increased wait time (10 minutes) for approval
    start = time.time()
    is_approved = False

    # Only one login attempt
    print("[!] Trying login...")
    result = get_access_token(email, password)

    if "access_token" in result:
        token = result["access_token"]
        slow(f"\n[✓] Token Extracted Successfully!\n[>] Token: {token}", 0.03)
        with open("fb_token.txt", "w") as f:
            f.write(token)
        print("[+] Token saved to fb_token.txt")
    elif "error_msg" in result and "www.facebook.com" in result["error_msg"]:
        # Wait for approval
        print("[✗] Login Blocked: User must verify their account.")
        slow("[~] Waiting for approval... This process will continue until approval is granted.", 0.03)

        while True:
            elapsed = time.time() - start
            if elapsed > max_wait:
                slow("\n[✗] Timed out waiting for approval. Try again later.", 0.04)
                break
            result = get_access_token(email, password)
            if "access_token" in result:
                token = result["access_token"]
                slow(f"\n[✓] Token Extracted Successfully!\n[>] Token: {token}", 0.03)
                with open("fb_token.txt", "w") as f:
                    f.write(token)
                print("[+] Token saved to fb_token.txt")
                break
            time.sleep(5)  # Waiting time before retrying to avoid detection
    else:
        slow(f"[✗] Login Failed: {result.get('error_msg', 'Unknown error')}", 0.04)

if __name__ == "__main__":
    main()
