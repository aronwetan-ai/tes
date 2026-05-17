/**
 * Telegram Bot Template — Runnable
 *
 * Usage:
 *   1. cp .env.example .env
 *   2. Set TOKEN=... (get from @BotFather)
 *   3. npm install node-telegram-bot-api dotenv
 *   4. node tools/templates/telegram_bot.js
 *
 * For production: pm2 start tools/templates/telegram_bot.js --name <bot-name>
 *
 * Source: Adapted from SUPERAGENT v2 m4.md
 */

require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');

const TOKEN = process.env.TOKEN;
if (!TOKEN) {
  console.error('ERROR: TOKEN env var missing. Set in .env file.');
  process.exit(1);
}

const bot = new TelegramBot(TOKEN, { polling: true });

console.log('✅ Bot online. Polling for messages...');

// /start
bot.onText(/\/start/, (msg) => {
  bot.sendMessage(
    msg.chat.id,
    '✅ Online.\n\nAvailable commands:\n/help — show all commands\n/status — system status'
  );
});

// /help
bot.onText(/\/help/, (msg) => {
  bot.sendMessage(
    msg.chat.id,
    '*Commands:*\n' +
    '/start — bot greeting\n' +
    '/help — this menu\n' +
    '/status — current status\n' +
    '/run [cmd] — execute command',
    { parse_mode: 'Markdown' }
  );
});

// /status
bot.onText(/\/status/, (msg) => {
  bot.sendMessage(
    msg.chat.id,
    `📊 *Status*\nTime: ${new Date().toISOString()}\nUptime: ${process.uptime()}s`,
    { parse_mode: 'Markdown' }
  );
});

// /run <command>
bot.onText(/\/run (.+)/, (msg, match) => {
  const command = match[1];
  // PRODUCTION: validate user against allowlist before executing
  bot.sendMessage(msg.chat.id, `Received: \`${command}\``, { parse_mode: 'Markdown' });
});

// Generic message handler (non-commands)
bot.on('message', (msg) => {
  if (msg.text && !msg.text.startsWith('/')) {
    bot.sendMessage(msg.chat.id, `Echo: "${msg.text}"`);
  }
});

// Error handling
bot.on('polling_error', (err) => {
  console.error('Polling error:', err.message);
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\nShutting down bot...');
  bot.stopPolling();
  process.exit(0);
});
