const { makeWASocket, useSingleFileAuthState, fetchLatestBaileysVersion, DisconnectReason } = require('@whiskeysockets/baileys');
const { Boom } = require('@hapi/boom');
const chalk = require('chalk');
const fs = require('fs');
const path = require('path');

const { state, saveState } = useSingleFileAuthState('./auth.json');

let delay = 5000; // delay in milliseconds (change to 10000 for 10 sec)

async function startBot() {
    const { version, isLatest } = await fetchLatestBaileysVersion();
    const sock = makeWASocket({
        version,
        auth: state,
        printQRInTerminal: true,
    });

    sock.ev.on('creds.update', saveState);

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect } = update;
        if (connection === 'close') {
            const shouldReconnect = (lastDisconnect.error)?.output?.statusCode !== DisconnectReason.loggedOut;
            console.log(chalk.red(`Connection closed. Reconnecting: ${shouldReconnect}`));
            if (shouldReconnect) startBot();
        } else if (connection === 'open') {
            console.log(chalk.green('✅ Connected to WhatsApp!'));
            startSpamming(sock);
        }
    });
}

function startSpamming(sock) {
    const numbers = fs.readFileSync('./numbers.txt', 'utf-8').split('\n').map(n => n.trim()).filter(n => n);
    const messages = fs.readFileSync('./messages.txt', 'utf-8').split('\n').filter(line => line.trim() !== '');

    let index = 0;

    const sendLoop = async () => {
        const msg = messages[index % messages.length];
        for (let num of numbers) {
            const jid = num + '@s.whatsapp.net';
            try {
                await sock.sendMessage(jid, { text: msg });
                console.log(chalk.blue(`✅ Sent to ${num}: ${msg}`));
            } catch (err) {
                console.log(chalk.red(`❌ Failed to send to ${num}: ${err.message}`));
            }
        }

        index++;
        setTimeout(sendLoop, delay);
    };

    sendLoop();
}

startBot();

