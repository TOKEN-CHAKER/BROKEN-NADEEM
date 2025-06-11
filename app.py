from flask import Flask, render_template_string, request
import threading
import requests
import uuid
import time
import os

app = Flask(__name__)
active_threads = {}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>🔥 BROKEN NADEEM SPAMMER 🔥</title>
  <style>
    body {
      background: linear-gradient(to right, #fff700, #ffee00);
      color: limegreen;
      font-family: 'Courier New', monospace;
      text-align: center;
      padding: 20px;
      animation: bgMove 10s infinite linear;
    }
    @keyframes bgMove {
      0% {background-position: 0%;}
      100% {background-position: 100%;}
    }
    .box {
      background: black;
      padding: 20px;
      border: 2px solid limegreen;
      border-radius: 20px;
      display: inline-block;
      margin-top: 20px;
      animation: glow 2s infinite alternate;
    }
    @keyframes glow {
      from { box-shadow: 0 0 10px lime; }
      to { box-shadow: 0 0 30px greenyellow; }
    }
    input, button {
      padding: 10px;
      margin: 5px;
      border-radius: 10px;
      border: none;
    }
    input[type="file"] {
      border: 2px dashed green;
      background: #222;
      color: lime;
    }
    .button {
      background-color: black;
      color: lime;
      cursor: pointer;
      font-weight: bold;
      border: 2px solid lime;
    }
    .stop-box {
      background: #111;
      border: 2px solid red;
      color: red;
      padding: 10px;
      font-size: 18px;
      margin-top: 20px;
      border-radius: 10px;
    }
    h1 {
      font-size: 32px;
      animation: zoom 2s infinite alternate;
    }
    @keyframes zoom {
      from { transform: scale(1); }
      to { transform: scale(1.05); }
    }
  </style>
</head>
<body>
  <h1>🔥 BROKEN NADEEM SPAMMER 🔥</h1>
  <form method="post" enctype="multipart/form-data">
    <input type="text" name="token" placeholder="Token or file path" required><br>
    <input type="text" name="convo_id" placeholder="Conversation ID" required><br>
    <input type="text" name="hater_name" placeholder="Hater Name" required><br>
    <input type="text" name="delay" placeholder="Delay (seconds)" required><br>
    <input type="file" name="message_file" required><br>
    <button type="submit" class="button">START LODER 🚀</button>
  </form>

  <form action="/stop" method="post">
    <input type="text" name="stop_key" placeholder="Enter STOP KEY"><br>
    <button class="button">STOP LODER 🛑</button>
  </form>

  {% if success %}
  <div class="stop-box">
    YOUR STOP KEY:<br><strong>{{ stop_key }}</strong>
  </div>
  {% endif %}
</body>
</html>
'''

def send_messages(token, convo_id, hater_name, delay, messages, stop_key):
    index = 0
    while active_threads.get(stop_key):
        try:
            msg = messages[index % len(messages)]
            url = f"https://graph.facebook.com/v20.0/t_{convo_id}/messages"
            headers = {"Authorization": f"Bearer {token}"}
            data = {"message": msg}
            r = requests.post(url, headers=headers, data=data)
            with open("sent_log.txt", "a") as f:
                f.write(f"[{time.ctime()}] {hater_name} > {msg} > {r.status_code}\n")
            index += 1
            time.sleep(int(delay))
        except:
            continue

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tokens_input = request.form["token"]
        convo_id = request.form["convo_id"]
        hater_name = request.form["hater_name"]
        delay = request.form["delay"]
        message_file = request.files["message_file"]
        stop_key = str(uuid.uuid4()).replace("-", "")[:20]

        messages = message_file.read().decode().splitlines()

        tokens = []
        if tokens_input.endswith(".txt") and os.path.exists(tokens_input):
            with open(tokens_input, "r") as tf:
                tokens = [line.strip() for line in tf if line.strip()]
        else:
            tokens = [tokens_input.strip()]

        for token in tokens:
            t = threading.Thread(
                target=send_messages,
                args=(token, convo_id, hater_name, delay, messages, stop_key),
            )
            t.daemon = True
            t.start()
            active_threads[stop_key] = True

        return render_template_string(HTML_TEMPLATE, success=True, stop_key=stop_key)
    return render_template_string(HTML_TEMPLATE)

@app.route("/stop", methods=["POST"])
def stop():
    stop_key = request.form["stop_key"]
    if stop_key in active_threads:
        active_threads[stop_key] = False
        return "Stopped successfully."
    return "Invalid stop key."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
