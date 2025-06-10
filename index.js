import { makeWASocket, useMultiFileAuthState, DisconnectReason, delay } from "@whiskeysockets/baileys";
import fs from "fs";
import pino from "pino";
import readline from "readline";
import os from "os";
import crypto from "crypto";
import axios from "axios";
import { exec } from "child_process";

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise((res) => rl.question(q, res));
let targets = [];
let groups = [];
let messages = [];
let senderPrefix = "";
let interval = 0;
let resumeIndex = 0;

function showBanner() {
    console.clear();
    console.log(`
\033[1;37m**    __ _           _                         
/ / /\\ \\ |**   __ *| |* ___  __ _ _ __  _ __  
\\ \\/  \\/ / '* \\ / *\` | __/ __|/ _\` | '* \\| '* \\ 
 \\  /\\  /| | | | (*| | |\\** \\ (*| | |*) | |*) |
  \\/  \\/ |*| |*|\\__,*|\\**|***/\\__,*| .**/| .**/ 
                                   |*|   |_|    

<<==============================>>
OWNER     : \033[1;33mBROKEN NADEEM
TOOL      : \033[1;32mAUTO WHATSAPP MESSAGE SENDER
PASSWORD  : \033[1;31mPROTECTED (BROKEN)
<<==============================>>\033[0m`);
}

async function startMessaging(sock) {
    while (true) {
        for (let i = resumeIndex; i < messages.length; i++) {
            try {
                const fullMessage = `${senderPrefix} ${messages[i]}`;
                const time = new Date().toLocaleTimeString();
                if (targets.length) {
                    for (const number of targets) {
                        await sock.sendMessage(`${number}@c.us`, { text: fullMessage });
                        console.log(`\033[1;32m[${time}] Sent to ${number}: ${fullMessage}`);
                    }
                } else {
                    for (const group of groups) {
                        await sock.sendMessage(`${group}@g.us`, { text: fullMessage });
                        console.log(`\033[1;32m[${time}] Sent to group ${group}: ${fullMessage}`);
                    }
                }
                await delay(interval * 1000);
            } catch (err) {
                console.error("\033[1;31mError sending message: ", err.message);
                resumeIndex = i;
                await delay(5000);
            }
        }
        resumeIndex = 0;
    }
}

async function initSocket() {
    const { state, saveCreds } = await useMultiFileAuthState("./auth_info");
    const sock = makeWASocket({ logger: pino({ level: "silent" }), auth: state });

    if (!sock.authState.creds.registered) {
        showBanner();
        const phone = await ask("\033[1;36m[+] Enter Your Phone Number: \033[0m");
        const code = await sock.requestPairingCode(phone);
        showBanner();
        console.log("\033[1;33mYour Pairing Code =>", code, "\033[0m");
    }

    sock.ev.on("creds.update", saveCreds);

    sock.ev.on("connection.update", async ({ connection, lastDisconnect }) => {
        if (connection === "open") {
            showBanner();
            console.log("\033[1;32m[+] WhatsApp Connected Successfully!\033[0m");
            const choice = await ask("[1] Send to Numbers\n[2] Send to Groups\nChoose Option: ");

            if (choice === "1") {
                const count = await ask("\033[1;33mHow many numbers? \033[0m");
                for (let i = 0; i < Number(count); i++) {
                    const num = await ask(`Enter Number ${i + 1}: `);
                    targets.push(num.trim());
                }
            } else if (choice === "2") {
                const allGroups = await sock.groupFetchAllParticipating();
                const groupIDs = Object.keys(allGroups);
                console.log("\nAvailable Groups:");
                groupIDs.forEach((id, idx) => {
                    console.log(`[${idx + 1}] ${allGroups[id].subject} | UID: ${id}`);
                });
                const count = await ask("\nHow many groups to target? ");
                for (let i = 0; i < Number(count); i++) {
                    const gid = await ask(`Enter Group UID ${i + 1}: `);
                    groups.push(gid.trim());
                }
            }

            const file = await ask("\033[1;36mEnter Message File Path: \033[0m");
            if (!fs.existsSync(file)) {
                console.error("\033[1;31mMessage file not found.\033[0m");
                process.exit(1);
            }
            messages = fs.readFileSync(file, "utf-8").split("\n").filter(Boolean);
            senderPrefix = await ask("\033[1;36mEnter Prefix (like Hater Name): \033[0m");
            interval = Number(await ask("\033[1;36mEnter Delay in seconds: \033[0m"));
            console.log("\n\033[1;32mAll inputs accepted. Starting Messaging...\033[0m");
            await startMessaging(sock);
        }

        if (connection === "close") {
            const code = lastDisconnect?.error?.output?.statusCode;
            if (code !== DisconnectReason.loggedOut) {
                console.log("\033[1;33mReconnecting in 5 seconds...\033[0m");
                setTimeout(() => initSocket(), 5000);
            } else {
                console.error("\033[1;31mLogged Out. Please restart the script.\033[0m");
            }
        }
    });
}

async function main() {
    showBanner();
    const password = await ask("\033[1;35mEnter Script Password: \033[0m");
    if (password !== "BROKEN") {
        console.log("\033[1;31mWrong Password! Exiting...\033[0m");
        process.exit(1);
    }
    await initSocket();
}

main();

process.on("uncaughtException", (err) => {
    if (
        err.message.includes("Socket connection timeout") ||
        err.message.includes("rate-overlimit")
    ) return;
    console.error("\n\033[1;31mUncaught Exception: ", err, "\033[0m");
});
