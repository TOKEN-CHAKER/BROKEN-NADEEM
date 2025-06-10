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
    const qrcode = (await import("qrcode-terminal"));
    const readline = (await import("readline")).createInterface({
      input: process.stdin,
      output: process.stdout
    });

    const ask = q => new Promise(res => readline.question(q, res));

    const banner = () => {
      console.clear();
      console.log(`\x1b[1;37m
__    __ _           _                         
/ /\\ /\\ \\ |__   __ _| |_ ___  __ _ _ __  _ __  
\\ \\/  \\/ / '_ \\ / _\` | __/ __|/ _\` | '_ \\| '_ \\ 
 \\  /\\  /| | | | (_| | |_\\__ \\ (_| | |_) | |_) |
  \\/  \\/ |_| |_|\\__,_|\\__|___/\\__,_| .__/| .__/ 
                                   |_|   |_|    
<<============================================================>>
[💀] OWNER   : \x1b[1;33mBROKEN NADEEM
[🔥] TOOL    : \x1b[1;32mNONSTOP WHATSAPP MESSAGE SENDER - 1 YEAR VERSION
<<============================================================>>\x1b[0m`);
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
                console.log("\x1b[1;30mTARGET =>>", number);
              }
            } else {
              for (const gid of groupIDs) {
                await sock.sendMessage(`${gid}@g.us`, { text: finalMessage });
                console.log("\x1b[1;32mGROUP UID =>>", gid);
              }
            }
            console.log("\x1b[1;32mTIME =", time);
            console.log("\x1b[1;37mSENT =>>", finalMessage);
            await delay(delaySec * 1000);
          } catch (err) {
            console.log("\x1b[1;33mError:", err.message, "- Retrying...");
            resumeIndex = i;
            await delay(5000);
          }
        }
        resumeIndex = 0;
      }
    }

    async function connectToWhatsApp(qrMode = true) {
      const sock = makeWASocket({
        logger: pino({ level: "silent" }),
        auth: state,
        printQRInTerminal: false,
        getMessage: async (msg) => {
          if (msg.qr && qrMode) {
            fs.writeFileSync("qr.txt", msg.qr);
            console.log("\x1b[1;36m[QR] Saved in qr.txt. Also displaying below:");
            qrcode.generate(msg.qr, { small: true });
          }
        }
      });

      sock.ev.on("connection.update", async ({ connection, lastDisconnect }) => {
        if (connection === "open") {
          banner();
          console.log("\n\x1b[1;32m[+] LOGIN SUCCESSFUL ❣️\n");

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
          console.log("\x1b[1;32m[✓] All set! Sending messages...\n");
          await sendMessages(sock);
        }

        if (connection === "close") {
          const reason = lastDisconnect?.error?.output?.statusCode;
          console.log("\x1b[1;31m[!] Disconnected. Reason:", reason);
          if (reason !== DisconnectReason.loggedOut) {
            console.log("\x1b[1;33m[~] Reconnecting in 5 seconds...\n");
            setTimeout(() => connectToWhatsApp(qrMode), 5000);
          } else {
            console.log("\x1b[1;31m[!] Logged Out. Restart the script and relogin.");
          }
        }
      });

      sock.ev.on("creds.update", saveCreds);
    }

    const password = await ask("Enter Password To Access Tool: ");
    if (password === "BROKEN") {
      banner();
      console.log("\x1b[1;32m[✓] Password Correct ✅\n");
      const method = await ask("[1] Login Using Existing Code\n[2] Login via QR Code\n=> ");
      await connectToWhatsApp(method === "2");
    } else {
      console.log("\x1b[1;31m[✗] Incorrect Password ❌\n");
      process.exit(1);
    }

    process.on("uncaughtException", err => {
      if (String(err).includes("Socket connection timeout") || String(err).includes("rate-overlimit")) return;
      console.error("Unexpected Error:", err);
    });

  } catch (e) {
    console.error("Startup Error:", e);
  }
})();
