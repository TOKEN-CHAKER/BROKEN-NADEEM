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
        "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
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
    email = input("[?] Facebook Email daalo: ")
    password = input("[?] Facebook Password daalo: ")

    print("\n[!] Login try ho raha hai...")

    result = get_access_token(email, password)

    # Access Token mil gaya
    if "access_token" in result:
        token = result["access_token"]
        slow(f"\n[✓] Token mil gaya!\n[>] Token: {token}", 0.03)
        with open("fb_token.txt", "w") as f:
            f.write(token)
        print("[+] Token fb_token.txt mein save ho gaya hai.")
    
    # Manual Approval Required
    elif "error_msg" in result and "www.facebook.com" in result["error_msg"]:
        slow("\n[!] Login Blocked: Approval chahiye.", 0.03)
        slow("[~] Manual approval do. Script wait karega jab tak approval milta nahi.", 0.03)
        
        while True:
            result = get_access_token(email, password)
            if "access_token" in result:
                token = result["access_token"]
                slow(f"\n[✓] Approval ke baad token mil gaya!\n[>] Token: {token}", 0.03)
                with open("fb_token.txt", "w") as f:
                    f.write(token)
                print("[+] Token fb_token.txt mein save ho gaya hai.")
                break
            time.sleep(5)

    # Unknown ya custom error
    else:
        error_msg = result.get("error_msg", "Kuch unknown error aaya (1).")
        slow(f"\n[✗] Login Failed: {error_msg}", 0.04)

if __name__ == "__main__":
    main()
