import os
import time
import random
import requests
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By

# Custom Broken Nadeem logo
def show_logo():
    os.system("clear")
    logo = """
╔═══════════════════════════════════════╗
║         BROKEN NADEEM TOOL            ║
║    Auto Login | Bypass | Token Dump   ║
╚═══════════════════════════════════════╝
"""
    print(logo)
    time.sleep(1)

# Token Extractor Function
def extract_token(email, password):
    show_logo()
    print(f"[~] Logging in with {email}...")

    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)

    try:
        driver.get("https://mbasic.facebook.com/login")
        time.sleep(2)

        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "pass").send_keys(password)
        driver.find_element(By.NAME, "login").click()
        time.sleep(3)

        current_url = driver.current_url

        if "save-device" in current_url or "home" in current_url:
            print("[✓] Login successful. Extracting token...")

            cookies = driver.get_cookies()
            cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

            headers = {
                "User-Agent": "Mozilla/5.0",
                "Cookie": cookie_string
            }

            response = requests.get("https://business.facebook.com/business_locations", headers=headers)
            token = None
            for line in response.text.splitlines():
                if "EAAG" in line:
                    token = line.strip().split('"')[1]
                    break

            if token:
                print(f"[TOKEN] {token}")
                with open("token.txt", "w") as f:
                    f.write(token)
            else:
                print("[!] Token not found.")

        elif "checkpoint" in current_url:
            print("[!] Checkpoint detected. Waiting for approval...")
            wait_for_approval(driver, email, password)
        else:
            print("[✗] Login failed.")

    except Exception as e:
        print("[ERROR]", str(e))
    finally:
        driver.quit()

# Wait + Retry if checkpoint
def wait_for_approval(driver, email, password):
    try:
        while True:
            print("[!] PLEASE APPROVE LOGIN ON FACEBOOK APP...")
            time.sleep(5)
            driver.refresh()
            if "save-device" in driver.current_url or "home" in driver.current_url:
                print("[✓] Approved successfully!")
                extract_token(email, password)
                break
    except Exception as err:
        print("[ERROR]", err)

# Main Entry
if __name__ == "__main__":
    show_logo()
    email = input("[+] Enter Facebook Email/Phone: ")
    password = input("[+] Enter Facebook Password: ")
    extract_token(email, password)
