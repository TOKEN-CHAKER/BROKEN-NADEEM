(async () => {
  try {
    const {
      makeWASocket,
      useMultiFileAuthState,
      delay,
      DisconnectReason
    } = await import("@whiskeysockets/baileys");
    const fs = await import("fs");
    const pino = (await import("pino")).default;
    const readline = (await import("readline")).createInterface({
      input: process.stdin,
      output: process.stdout
    });
    const os = await import("os");
    const crypto = await import("crypto");
    const { exec } = await import("child_process");

    const question = (text) => new Promise(resolve => readline.question(text, resolve));
    const banner = () => {
      console.clear();
      console.log(`
\033[1;37m__    __ _           _                         
/ /\\ /\\ \\ |__   __ _| |_ ___  __ _ _ __  _ __  
\\ \\/  \\/ / '_ \\ / _\` | __/ __|/ _\` | '_ \\| '_ \\ 
 \\  /\\  /| | | | (_| | |\\__ \\ (_| | |_) | |_) |
  \\/  \\/ |_| |_|\\__,_|\\__|___/\\__,_| .__/| .__/ 
                                   |_|   |_|    

<<=============================================>>
[🔒] OWNER   : BROKEN NADEEM
[💀] TOOL    : AUTOMATIC WHATSAPP MESSAGE SENDER
[🛡️] STATUS  : NONSTOP RUNNING MODE
<<=============================================>>`);
    };

    const hash = crypto.createHash("sha256").update(os.platform() + os.userInfo().username).digest("hex");
    banner();
    const password = await question("ENTER PASSWORD TO START: ");
    if (password.trim() !== "BROKEN") {
      console.log("\n\033[1;31m❌ WRONG PASSWORD. ACCESS DENIED.\n");
      process.exit(1);
    }

    let targets = [], groups = [], messageLines = [], messagePrefix = "", delaySeconds = 0, currentIndex = 0;

    const { state, saveCreds } = await useMultiFileAuthState("./auth_info");

    async function sendMessages(sock) {
      while (true) {
        for (let i = currentIndex; i < messageLines.length; i++) {
          try {
            const fullMsg = messagePrefix + " " + messageLines[i];
            const time = new Date().toLocaleTimeString();
            if (targets.length > 0) {
              for (const number of targets) {
                await sock.sendMessage(number + "@c.us", { text: fullMsg });
                console.log(`📤 SENT TO: ${number} at ${time}`);
              }
            } else {
              for (const group of groups) {
                await sock.sendMessage(group + "@g.us", { text: fullMsg });
                console.log(`📤 SENT TO GROUP: ${group} at ${time}`);
              }
            }
            await delay(delaySeconds * 1000);
          } catch (err) {
            console.error("⚠️ SEND ERROR: ", err.message);
            currentIndex = i;
            await delay(5000);
          }
        }
        currentIndex = 0; // Restart after end
      }
    }

    const startBot = async () => {
      const sock = makeWASocket({
        logger: pino({ level: "silent" }),
        auth: state
      });

      if (!sock.authState.creds.registered) {
        banner();
        const number = await question("[📲] ENTER PHONE NUMBER (with country code): ");
        const code = await sock.requestPairingCode(number);
        banner();
        console.log("🔗 YOUR PAIRING CODE =>", code);
      }

      sock.ev.on("connection.update", async ({ connection, lastDisconnect }) => {
        if (connection === "open") {
          banner();
          console.log("✅ CONNECTED TO WHATSAPP ✅\n");
          const mode = await question("1️⃣ Send to Target Number\n2️⃣ Send to Group\nChoose Option [1/2]: ");
          if (mode === "1") {
            const count = parseInt(await question("📱 HOW MANY TARGET NUMBERS? "));
            for (let i = 0; i < count; i++) {
              const target = await question(`🔢 ENTER TARGET ${i + 1}: `);
              targets.push(target);
            }
          } else {
            const allGroups = await sock.groupFetchAllParticipating();
            const groupList = Object.keys(allGroups);
            console.log("\n📃 GROUP LIST:");
            groupList.forEach((id, i) => {
              console.log(`[${i + 1}] ${allGroups[id].subject} [ID: ${id}]`);
            });
            const gCount = parseInt(await question("\n📦 HOW MANY GROUPS TO USE? "));
            for (let i = 0; i < gCount; i++) {
              const gid = await question(`📥 ENTER GROUP UID ${i + 1}: `);
              groups.push(gid);
            }
          }

          const msgPath = await question("📄 ENTER MESSAGE FILE PATH: ");
          messageLines = fs.readFileSync(msgPath, "utf-8").split("\n").filter(Boolean);
          messagePrefix = await question("😈 ENTER HATER NAME / PREFIX: ");
          delaySeconds = parseInt(await question("⏱️ ENTER DELAY (seconds): "));

          banner();
          console.log("\n🚀 STARTING MESSAGE SENDING...\n");
          await sendMessages(sock);
        }

        if (connection === "close") {
          const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
          console.log("⚠️ DISCONNECTED. RETRYING IN 5s...");
          if (shouldReconnect) setTimeout(startBot, 5000);
          else console.log("❌ LOGGED OUT. PLEASE RESTART.");
        }
      });

      sock.ev.on("creds.update", saveCreds);
    };

    process.on("uncaughtException", err => {
      const msg = String(err);
      if (msg.includes("Socket") || msg.includes("rate-overlimit")) return;
      console.log("⚠️ UNCAUGHT ERROR: ", err);
    });

    await startBot();

  } catch (e) {
    console.error("❌ ERROR STARTING SCRIPT:", e);
  }
})();
