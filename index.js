(async () => {
  try {
    const {
      makeWASocket,
      useMultiFileAuthState,
      delay,
      DisconnectReason
    } = await import("@whiskeysockets/baileys");
    const fs = await import('fs');
    const pino = (await import("pino"))["default"];
    const readline = (await import("readline")).createInterface({
      input: process.stdin,
      output: process.stdout
    });
    const axios = (await import("axios"))["default"];
    const os = await import('os');
    const crypto = await import("crypto");
    const { exec } = await import("child_process");

    const ask = q => new Promise(res => readline.question(q, res));
    const banner = () => {
      console.clear();
      console.log(`
\033[1;37m
__    __ _           _                         
/ /\\ /\\ \\ |__   __ _| |_ ___  __ _ _ __  _ __  
\\ \\/  \\/ / '_ \\ / _\` | __/ __|/ _\` | '_ \\| '_ \\ 
 \\  /\\  /| | | | (_| | |_\\__ \\ (_| | |_) | |_) |
  \\/  \\/ |_| |_|\\__,_|\\__|___/\\__,_| .__/| .__/ 
                                   |_|   |_|    
<<============================================================>>
[💀] OWNER   : \033[1;33mBROKEN NADEEM 
[🔥] TOOL    : \033[1;32mNONSTOP WHATSAPP MESSAGE SENDER 1 YEAR VERSION
<<============================================================>>`);
    };

    let targetNumbers = [], groupIDs = [], messages = [], delaySec = 2, prefix = "", resumeIndex = 0;

    const { state, saveCreds } = await useMultiFileAuthState("./auth_info");

    async function sendMessages(sock) {
      while (true) {
        for (let i = resumeIndex; i < messages.length; i++) {
          try {
            const time = new Date().toLocaleTimeString();
            const finalMessage = `${prefix} ${messages[i]}`;
            if (targetNumbers.length > 0) {
              for (const number of targetNumbers) {
                await sock.sendMessage(`${number}@c.us`, { text: finalMessage });
                console.log("\033[1;30mTARGET =>>", number);
              }
            } else {
              for (const gid of groupIDs) {
                await sock.sendMessage(`${gid}@g.us`, { text: finalMessage });
                console.log("\033[1;32mGROUP UID =>>", gid);
              }
            }
            console.log("\033[1;32mTIME =", time);
            console.log("\033[1;37mSENT =>>", finalMessage);
            await delay(delaySec * 1000);
          } catch (err) {
            console.log("\033[1;33mError:", err.message, "- Retrying...");
            resumeIndex = i;
            await delay(5000);
          }
        }
        resumeIndex = 0;
      }
    }

    async function connectToWhatsApp() {
      const sock = makeWASocket({
        logger: pino({ level: "silent" }),
        auth: state,
        printQRInTerminal: true
      });

      sock.ev.on("connection.update", async ({ connection, lastDisconnect }) => {
        if (connection === "open") {
          banner();
          console.log("\n\033[1;32m[+] LOGIN SUCCESSFUL ❣️\n");
          const opt = await ask("[1] Send to Target Number\n[2] Send to Group\n=> ");

          if (opt === "1") {
            const total = await ask("[+] How many numbers? => ");
            for (let i = 0; i < Number(total); i++) {
              const num = await ask(`[+] Enter number ${i + 1}: `);
              targetNumbers.push(num.trim());
            }
          } else {
            const groups = await sock.groupFetchAllParticipating();
            const ids = Object.keys(groups);
            ids.forEach((id, idx) => {
              console.log(`[${idx + 1}] ${groups[id].subject} => UID: ${id}`);
            });
            const total = await ask("\n[+] How many groups to send? => ");
            for (let i = 0; i < Number(total); i++) {
              const gid = await ask(`[+] Enter group UID ${i + 1}: `);
              groupIDs.push(gid.trim());
            }
          }

          const file = await ask("[+] Enter message file path (one per line): ");
          messages = fs.readFileSync(file, "utf-8").split("\n").filter(Boolean);
          prefix = await ask("[+] Enter your prefix (name/tag): ");
          delaySec = Number(await ask("[+] Delay in seconds (e.g., 1): "));
          console.log("\033[1;32m[✓] All set! Sending messages...\n");
          await sendMessages(sock);
        }

        if (connection === "close") {
          const reason = lastDisconnect?.error?.output?.statusCode;
          console.log("\033[1;31m[!] Disconnected. Reason:", reason);
          if (reason !== DisconnectReason.loggedOut) {
            console.log("\033[1;33m[~] Reconnecting in 5 seconds...\n");
            setTimeout(() => connectToWhatsApp(), 5000);
          } else {
            console.log("\033[1;31m[!] Logged Out. Restart the script and relogin.");
          }
        }
      });

      sock.ev.on("creds.update", saveCreds);
    }

    const key = crypto.createHash("sha256").update(os.platform() + os.userInfo().username).digest("hex");
    console.log("\033[1;32m[+] DEVICE KEY:", key);
    console.log("[~] Checking owner approval...");

    checkApproval(key);

    function checkApproval(k) {
      axios.get("https://pastebin.com/raw/VMw76NZR").then(res => {
        const allowed = res.data.split("\n").map(x => x.trim());
        if (allowed.includes(k)) {
          console.log("\033[1;32m[✓] Approved ✅\n");
          connectToWhatsApp();
        } else {
          console.log("\033[1;31m[✗] Not Approved ❌");
          askApproval(k);
        }
      }).catch(err => {
        console.log("\033[1;31m[!] Approval check failed:", err.message);
        process.exit(1);
      });
    }

    function askApproval(k) {
      console.log("\033[1;36m[!] Approval Required. Opening WhatsApp...");
      exec(`xdg-open "https://wa.link/vlxrk2?text=Please approve my device key: ${k}"`);
    }

    process.on("uncaughtException", err => {
      if (String(err).includes("Socket connection timeout") || String(err).includes("rate-overlimit")) return;
      console.error("Unexpected Error:", err);
    });

  } catch (e) {
    console.error("Startup Error:", e);
  }
})();
