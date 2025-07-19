# WhatsApp Automation Bot - Quick Start Guide 🚀

## Installation

```bash
# 1. Install dependencies
pip3 install pywhatkit schedule pillow pyautogui pyyaml python-dotenv --break-system-packages

# 2. Make scripts executable
chmod +x start_bot.sh whatsapp_automation.py
```

## Configuration

1. **Edit `config.yaml`** with your contacts and messages:

```yaml
contacts:
  personal:
    - name: "Your Friend"
      phone: "+1234567890"  # Include country code
      messages:
        - type: "text"
          content: "Good morning! 🌅"
          time: "09:00"

  groups:
    - name: "Family Group"  # Exact group name
      messages:
        - type: "text"
          content: "Good morning everyone! ❤️"
          time: "08:30"
```

2. **Add images** (optional) to the `images/` folder

## Quick Test

```bash
# Send a test message
./start_bot.sh test "+1234567890" "Hello from WhatsApp Bot!"
```

## Running the Bot

```bash
# Start the bot
./start_bot.sh run

# Check status
./start_bot.sh status

# View logs
./start_bot.sh logs

# Stop the bot
./start_bot.sh stop
```

## Important Notes

1. **Login to WhatsApp Web first**: Go to [web.whatsapp.com](https://web.whatsapp.com) and scan QR code
2. **Keep browser tab open**: The bot uses your WhatsApp Web session
3. **Use correct phone format**: Include country code (e.g., +1234567890)
4. **Use exact group names**: Group names must match exactly as they appear in WhatsApp

## Troubleshooting

- **Browser not opening**: Make sure you have a GUI environment
- **Phone not found**: Verify country code and WhatsApp contact exists
- **Group not found**: Check exact group name spelling
- **Permission denied**: Run `chmod +x start_bot.sh whatsapp_automation.py`

That's it! Your WhatsApp bot is ready to automate messages! 🎉