(async () => {
  const {
    makeWASocket,
    useMultiFileAuthState,
    delay,
    DisconnectReason
  } = await import("@whiskeysockets/baileys");
  const fs = await import('fs');
  const pino = (await import("pino")).default;
  const readline = (await import("readline")).createInterface({
    input: process.stdin,
    output: process.stdout
  });

  const question = q => new Promise(res => readline.question(q, res));

  const showBanner = () => {
    console.clear();
    console.log(`
\033[1;37m    __ _           _                         
/ /\ /\ \ |   __ | | ___  __ _ _ __  _ __  
\\ \/  \/ / ' \\ /  | __/ __|/ _ | ' \\| ' \\ 
 \\  /\\  /| | | | (| | |_\\__ \\ (| | |) | |) |
  \\/  \\/ |_| |_|\\__,_|\\__|___/\\__,_| .__/|_|
                                   |_|       
<<============================================================>>
[N+A] OWNER   : \033[1;33mBROKEN NADEEM [-\033[1;32mNO APPROVAL SYSTEM-] 
[A+N] GITHUB  : \033[1;31mBROKEN-NADEEM \033[1;35m[-\033[1;33m🔥💀TOOL UNLOCKED-]
[N+A] TOOL 💀 : \033[1;32mAUTOMATIC WHATSAPP MESSAGE \033[1;37mSENDER NADEEM HERE
<<============================================================>>`);
  };

  let targetNumbers = [];
  let groupUIDs = [];
  let messages = null;
  let delayTime = null;
  let haterName = null;
  let lastIndex = 0;

  const { state, saveCreds } = await useMultiFileAuthState("./auth_info");

  async function sendLoop(sock) {
    while (true) {
      for (let i = lastIndex; i < messages.length; i++) {
        try {
          const now = new Date().toLocaleTimeString();
          const message = `${haterName} ${messages[i]}`;

          if (targetNumbers.length > 0) {
            for (const number of targetNumbers) {
              await sock.sendMessage(`${number}@c.us`, { text: message });
              console.log("\033[1;30mTARGET NUMBER => " + number);
            }
          } else {
            for (const group of groupUIDs) {
              await sock.sendMessage(`${group}@g.us`, { text: message });
              console.log("\033[1;32mGROUP UID => \033[0m" + group);
            }
          }

          console.log("\033[1;32mTIME => " + now);
          console.log("\033[1;37mSENT => " + message);
          console.log("\033[1;32m[<<===========◀️━━•𖣐✿⊱ BROKEN NADEEM ⊰✿𖣐•━━▶️=========>>]");
          await delay(delayTime * 1000);
        } catch (err) {
          console.log("\033[1;33mError sending message: " + err.message + ". Retrying...\033[0m");
          lastIndex = i;
          await delay(5000);
        }
      }
      lastIndex = 0;
    }
  }

  const start = async () => {
    const sock = makeWASocket({
      logger: pino({ level: "silent" }),
      auth: state
    });

    if (!sock.authState.creds.registered) {
      showBanner();
      const phone = await question("[+] ENTER YOUR PHONE NUMBER => ");
      const code = await sock.requestPairingCode(phone);
      showBanner();
      console.log("YOUR PAIRING CODE => " + code);
    }

    sock.ev.on("connection.update", async ({ connection, lastDisconnect }) => {
      if (connection === "open") {
        showBanner();
        console.log("[+] YOUR WHATSAPP LOGIN ✅");

        const choice = await question("[1] \033[1;32mSEND TO TARGET NUMBER\n[2] \033[1;34mSEND TO WHATSAPP GROUP\n\033[1;32m[+] CHOOSE OPTION => ");
        
        if (choice === '1') {
          const total = await question("[+] \033[1;33mHOW MANY TARGET NUMBERS => ");
          for (let i = 0; i < total; i++) {
            const num = await question(`\033[1;32m[+] ENTER TARGET NUMBER ${i + 1} => `);
            targetNumbers.push(num);
          }
        } else if (choice === '2') {
          const groups = await sock.groupFetchAllParticipating();
          const ids = Object.keys(groups);
          console.log("WHATSAPP GROUPS =>>");
          ids.forEach((id, i) => {
            console.log(`\033[1;32m[${i + 1}] GROUP: \033[0m${groups[id].subject} \033[1;32mUID: \033[0m${id}`);
          });

          const total = await question("\033[1;34m[+] HOW MANY GROUPS TO TARGET => ");
          for (let i = 0; i < total; i++) {
            const uid = await question(`\033[1;32m[+] ENTER GROUP UID ${i + 1} => `);
            groupUIDs.push(uid);
          }
        }

        const filePath = await question("[+] ENTER MESSAGE FILE PATH => ");
        messages = fs.readFileSync(filePath, "utf-8").split("\n").filter(Boolean);

        haterName = await question("[+] ENTER HATER NAME => ");
        delayTime = await question("[+] ENTER MESSAGE DELAY (in sec) => ");

        console.log("\033[1;32mAll details collected.\033[0m");
        showBanner();
        console.log("NOW STARTING MESSAGE SENDING....");
        console.log("\033[1;32m[<<===============◀️━━•𖣐✿⊱ OWNER MR NADEEM ⊰✿𖣐•━━▶️==============>>]");
        await sendLoop(sock);
      }

      if (connection === "close" && lastDisconnect?.error) {
        const shouldReconnect = lastDisconnect.error?.output?.statusCode !== DisconnectReason.loggedOut;
        if (shouldReconnect) {
          console.log("NETWORK ISSUE, RETRYING in 5 SECONDS...");
          setTimeout(start, 5000);
        } else {
          console.log("Connection closed. Please restart the script.");
        }
      }
    });

    sock.ev.on("creds.update", saveCreds);
  };

  await start();
})();
