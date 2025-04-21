import sys
import os
import time

# Clear screen based on OS
def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

# Typewriter effect
def slow(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Logo for Broken Nadeem style
def logo():
    clear()
    print("\n")
    print("██████╗░██████╗░░█████╗░███████╗██╗░░██╗███████╗███╗░░██╗")
    print("██╔══██╗██╔══██╗██╔══██╗██╔════╝██║░░██║██╔════╝████╗░██║")
    print("██║░░██║██████╦╝██║░░██║█████╗░░███████║█████╗░░██╔██╗██║")
    print("██║░░██║██╔══██╗██║░░██║██╔══╝░░██╔══██║██╔══╝░░██║╚████║")
    print("██████╔╝██████╦╝╚█████╔╝███████╗██║░░██║███████╗██║░╚███║")
    print("╚═════╝░╚═════╝░░╚════╝░╚══════╝╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝")
    print("        » FAKE TOKEN SYSTEM - BROKEN NADEEM STYLE «")
    print("=========================================================\n")

# Fake Gmail/Password check
def fake_token_check(email, password):
    # Manually verified credentials
    valid_creds = {
        "example@gmail.com": "password123",
        "nadeem@broken.com": "brokenpass"
    }

    if email in valid_creds and password == valid_creds[email]:
        return {
            "access_token": f"FAKE_TOKEN_FOR_{email.upper().replace('@', '_AT_')}"
        }
    else:
        return {
            "error_msg": "Gmail ya password galat hai!"
        }

# Main login and control flow
def main():
    logo()
    email = input("[?] Gmail Address: ")
    password = input("[?] Gmail Password: ")

    print("\n[!] Gmail/Password verify ho raha hai...")

    result = fake_token_check(email, password)

    if "access_token" in result:
        token = result["access_token"]
        slow(f"\n[✓] Verification success!", 0.03)
        slow(f"[>] Fake Token: {token}", 0.03)
        with open("fake_fb_token.txt", "w") as f:
            f.write(token)
        print("[+] Token 'fake_fb_token.txt' mein save ho gaya hai.")
    else:
        slow(f"[✗] Error: {result['error_msg']}", 0.03)
        print("\n[!] Verification failed. Try again.")

if __name__ == "__main__":
    main()
