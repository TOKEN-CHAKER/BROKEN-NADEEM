import time
import random
import os
import sys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

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

def main():
    logo()
    email = input("[?] Enter Facebook Email: ")
    password = input("[?] Enter Facebook Password: ")

    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)

    try:
        driver.get("https://mbasic.facebook.com")
        time.sleep(2)

        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "pass").send_keys(password)
        driver.find_element(By.NAME, "login").click()

        time.sleep(5)

        if "save-device" in driver.page_source or "m_sess" in driver.current_url:
            slow("\n[✓] Logged in successfully! Trying to fetch token...", 0.03)

            driver.get("https://developers.facebook.com/tools/explorer")
            time.sleep(5)

            # Token fetching logic here (you can customize this part)
            slow("[✓] Token fetch simulated (add Graph API fetch logic here)", 0.02)
        else:
            slow("[✗] Login Failed! Check credentials or try manually approving checkpoint.", 0.03)

    except Exception as e:
        print(f"[!] Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
