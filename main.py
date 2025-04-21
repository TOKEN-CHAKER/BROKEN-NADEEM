import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import os

# Function to extract token from cookie
def extract_token(cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10)',
        'Cookie': cookie
    }
    try:
        res = requests.get("https://business.facebook.com/business_locations", headers=headers)
        if "accessToken" in res.text:
            token = res.text.split('accessToken":"')[1].split('"')[0]
            return token
        else:
            return None
    except Exception as e:
        return f"Error: {str(e)}"

# Load cookie from file
def load_cookie():
    filepath = filedialog.askopenfilename(title="Select Cookie File", filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, 'r') as f:
            cookie_text.set(f.read().strip())

# Get token and handle UI
def get_token():
    cookie = cookie_text.get()
    if not cookie:
        messagebox.showerror("Error", "Please provide a cookie")
        return

    token = extract_token(cookie)
    if token and token.startswith("EAA"):
        result_text.set(f"Token Extracted:\n{token}")
        with open("fb_token.txt", "w") as f:
            f.write(token)
        messagebox.showinfo("Success", "Token saved to fb_token.txt")
    else:
        result_text.set("Failed to extract token. Invalid cookie or blocked session.")

# GUI setup
root = tk.Tk()
root.title("FB Cookie Token Extractor - Broken Nadeem Style")
root.geometry("600x400")
root.resizable(False, False)

cookie_text = tk.StringVar()
result_text = tk.StringVar()

# Widgets
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill=tk.BOTH, expand=True)

tk.Label(frame, text="Enter Facebook Cookie:", font=("Arial", 12)).pack(anchor='w')
tk.Entry(frame, textvariable=cookie_text, font=("Courier", 10), width=80).pack(pady=5)

btn_frame = tk.Frame(frame)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Load from File", command=load_cookie, width=20).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Extract Token", command=get_token, width=20, bg="green", fg="white").grid(row=0, column=1, padx=10)

result_label = tk.Label(frame, textvariable=result_text, wraplength=550, justify="left", fg="blue", font=("Courier", 10))
result_label.pack(pady=10)

root.mainloop()
