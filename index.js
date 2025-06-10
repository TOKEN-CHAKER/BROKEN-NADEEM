import {
  makeWASocket,
  useMultiFileAuthState,
  delay,
  DisconnectReason
} from "@whiskeysockets/baileys";

import fs from "fs";
import readline from "readline";
import pino from "pino";
import os from "os";
import crypto from "crypto";

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const ask = (query) => new Promise((resolve) => rl.question(query, resolve));

const banner = () => {
  console.clear();
  console.log(
    '\n\x1b[1;37m**    __ _           _                         \n/ / /\\ \\ |__   __ _| |_ ___  __ _ _ __  _ __  \n\\ \\/  \\/ / _ \\ / _` | __/ __|/ _` | \'_ \\| \'_ \\ \n \\  /\\  /  __/ | (_| | |_\\__ \\ (_| | |_) | |_) |\n  \\/  \\/ \\___|_|\\__,_|\\__|___/\\__,_| .__/| .__/ \n                                   |_|   |_|    \x1b[0m'
  );
  console.log(
    "<<============================================================>>"
  );
  console.log("\x1b[1;33m[+] OWNER   : BROKEN NADEEM");
  console.log("\x1b[1;31m[+] TOOL    : WHATSAPP AUTO MESSAGE SENDER");
  console.log("<<============================================================>>");
};

let targets = [];
let groupTargets = [];
let messages = [];
let delaySec = 5;
let prefixText = "";

process.on("uncaughtException", (err) => {
  console.log("\x1b[31m[ERROR]\x1b[0m", err.message);
});

async function sendMessages(sock) {
  let index = 0;
  while (true) {
    for (; index < messages.length; index++) {
      const text = `${prefixText} ${messages[index]}`;
      const timestamp = new Date().toLocaleTimeString();
      try {
        if (targets.length > 0) {
          for (const num of targets) {
            await sock.sendMessage(num + "@c.us", { text });
            console.log(`\x1b[1;36m[SENT to Number] ${num} => ${text}`);
          }
        } else {
          for (const gid of groupTargets) {
            await sock.sendMessage(gid + "@g.us", { text });
            console.log(`\x1b[1;35m[SENT to Group] ${gid} => ${text}`);
          }
        }
        console.log(`\x1b[1;32m[TIME] ${timestamp}`);
        await delay(delaySec * 1000);
      } catch (err) {
        console.log(`\x1b[33m[ERROR] ${err.message} — Retrying in 5s`);
        await delay(5000);
        break;
      }
    }
    index = 0;
  }
}

async function startSocket() {
  const { state, saveCreds } = await useMultiFileAuthState("./auth_info");
  const sock = makeWASocket({
    logger: pino({ level: "silent" }),
    auth: state
  });

  sock.ev.on("creds.update", saveCreds);

  sock.ev.on("connection.update", async (update) => {
    const { connection, lastDisconnect } = update;
    if (connection === "open") {
      banner();
      const option = await ask("[1] Send to Target Number\n[2] Send to Group\nChoose => ");

      if (option === "1") {
        const count = parseInt(await ask("How many numbers? => "));
        for (let i = 0; i < count; i++) {
          const num = await ask(`Enter number ${i + 1} => `);
          targets.push(num);
        }
      } else {
        const groups = await sock.groupFetchAllParticipating();
        const groupIds = Object.keys(groups);
        console.log("Your Groups:");
        groupIds.forEach((id, idx) => {
          console.log(`[${idx + 1}] ${groups[id].subject} => ${id}`);
        });

        const gcount = parseInt(await ask("How many groups? => "));
        for (let i = 0; i < gcount; i++) {
          const gid = await ask(`Enter Group ID ${i + 1} => `);
          groupTargets.push(gid);
        }
      }

      const filePath = await ask("Enter message file path => ");
      messages = fs.readFileSync(filePath, "utf-8").split("\n").filter(Boolean);
      prefixText = await ask("Enter prefix (e.g., target name) => ");
      delaySec = parseInt(await ask("Enter delay in seconds => "));

      banner();
      console.log("\x1b[1;32m[+] SENDING MESSAGES...\x1b[0m");
      await sendMessages(sock);
    }

    if (connection === "close") {
      const shouldRetry = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
      if (shouldRetry) {
        console.log("Reconnecting in 5 seconds...");
        setTimeout(startSocket, 5000);
      } else {
        console.log("Logged out. Restart the script.");
      }
    }
  });
}

async function main() {
  banner();
  const userPass = await ask("Enter Password to continue => ");
  if (userPass !== "BROKEN") {
    console.log("\x1b[1;31m❌ WRONG PASSWORD. CONTACT BROKEN NADEEM.\x1b[0m");
    process.exit(1);
  }
  console.log("\x1b[1;32m✅ ACCESS GRANTED.\x1b[0m");
  await startSocket();
}

main();
