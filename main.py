import time
import sys
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver.v2 as uc

# Functions for displaying text
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

# Function to configure headless Chrome with undetected_chromedriver
def configure_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_argument("--remote-debugging-port=9222")
    
    driver = uc.Chrome(options=options)
    return driver

# Function to handle login and approval bypass
def login_and_approve(driver, email, password):
    driver.get("https://www.facebook.com/login")

    # Find and fill the login form
    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "pass")
    email_input.send_keys(email)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

    # Handle approval dialog if present
    try:
        approve_button = driver.find_element(By.XPATH, "//button[contains(text(),'Approve')]")
        approve_button.click()
        time.sleep(5)
    except:
        pass  # If no approval is required, continue

    # Check for successful login
    if "home" in driver.current_url:
        slow("[✓] Login Successful!", 0.03)
    else:
        slow("[✗] Login Failed!", 0.03)
        return None

    return driver

# Function to extract token from Facebook session
def extract_token(driver):
    driver.get("https://www.facebook.com")
    cookies = driver.get_cookies()

    for cookie in cookies:
        if cookie['name'] == 'c_user':
            return cookie['value']

    return None

# Main function to drive the script
def main():
    logo()
    email = input("[?] Enter Facebook Email: ")
    password = input("[?] Enter Facebook Password: ")

    # Configure and launch headless browser
    driver = configure_driver()

    # Log in and approve the session
    driver = login_and_approve(driver, email, password)
    if driver:
        # Extract token after approval
        token = extract_token(driver)
        if token:
            slow(f"\n[✓] Token Extracted Successfully!\n[>] Token: {token}", 0.02)
            with open("fb_token.txt", "w") as f:
                f.write(token)
            print("[+] Token saved to fb_token.txt")
        else:
            print("[✗] Failed to extract token!")
    driver.quit()

if __name__ == "__main__":
    main()
