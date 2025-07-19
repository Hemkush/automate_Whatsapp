# WhatsApp Automation Bot 🤖

A Python-based WhatsApp automation bot that can send scheduled messages to personal contacts and groups. Supports text messages, images with/without captions, and runs in the background with full scheduling capabilities.

## Features ✨

- 📱 **Text Messages**: Send automated text messages to individuals and groups
- 🖼️ **Image Messages**: Send images with or without captions
- ⏰ **Scheduling**: Daily scheduled messages at specific times
- 👥 **Groups & Contacts**: Support for both personal contacts and group messaging
- 🔄 **Background Operation**: Runs continuously in the background
- 📊 **Logging**: Comprehensive logging for monitoring and debugging
- ⚙️ **Configuration**: Easy YAML-based configuration
- 🔧 **Service Mode**: Can run as a system service (systemd)

## Prerequisites 📋

- Python 3.7 or higher
- A web browser (Chrome, Firefox, Safari, etc.)
- WhatsApp Web access
- Linux/macOS/Windows (tested on Linux)

## Quick Start 🚀

### 1. Setup the Bot

```bash
# Make the setup script executable
chmod +x start_bot.sh

# Run the setup
./start_bot.sh setup
```

### 2. Configure Your Contacts and Messages

Edit the `config.yaml` file with your contacts and desired messages:

```yaml
contacts:
  personal:
    - name: "John Doe"
      phone: "+1234567890"  # Include country code
      messages:
        - type: "text"
          content: "Good morning! Have a great day! 🌅"
          time: "09:00"
        - type: "image"
          image_path: "images/motivational_quote.jpg"
          caption: "Your daily motivation! 💪"
          time: "08:00"

  groups:
    - name: "Family Group"  # Exact group name as it appears in WhatsApp
      messages:
        - type: "text"
          content: "Good morning family! ❤️"
          time: "08:30"
```

### 3. Login to WhatsApp Web

**IMPORTANT**: Before running the bot, make sure you're logged into WhatsApp Web:

1. Open your browser
2. Go to [web.whatsapp.com](https://web.whatsapp.com)
3. Scan the QR code with your phone
4. Keep the tab open (the bot will use this session)

### 4. Test the Bot

Send a test message to verify everything works:

```bash
./start_bot.sh test "+1234567890" "Hello from WhatsApp Bot!"
```

### 5. Start the Bot

```bash
# Start in background
./start_bot.sh run

# Check status
./start_bot.sh status

# View live logs
./start_bot.sh logs

# Stop the bot
./start_bot.sh stop
```

## Configuration Guide 📝

### Contact Configuration

#### Personal Contacts
```yaml
personal:
  - name: "Contact Name"
    phone: "+1234567890"  # Must include country code
    messages:
      - type: "text"
        content: "Your message here"
        time: "09:00"  # 24-hour format
```

#### Group Messages
```yaml
groups:
  - name: "Exact Group Name"  # Must match exactly
    messages:
      - type: "text"
        content: "Group message"
        time: "08:30"
```

### Message Types

#### Text Messages
```yaml
- type: "text"
  content: "Your text message with emojis 😊"
  time: "09:00"
```

#### Image Messages
```yaml
- type: "image"
  image_path: "images/your_image.jpg"
  caption: "Optional caption text"  # Can be omitted
  time: "18:00"
```

### Settings Configuration

```yaml
settings:
  wait_time: 20           # Seconds to wait after opening WhatsApp
  close_tab: true         # Close browser tab after sending
  image_formats: [".jpg", ".jpeg", ".png", ".gif", ".webp"]
  retry_attempts: 3       # Number of retry attempts on failure
  retry_delay: 5          # Seconds between retries
```

## Usage Examples 💡

### Command Line Usage

```bash
# Setup and install dependencies
python3 setup.py

# Run the bot (with scheduling)
python3 whatsapp_automation.py run

# Send a test message
python3 whatsapp_automation.py test "+1234567890" "Test message"

# List scheduled jobs
python3 whatsapp_automation.py schedule
```

### Using the Launcher Script

```bash
# Setup
./start_bot.sh setup

# Run in background
./start_bot.sh run

# Test message
./start_bot.sh test "+1234567890" "Hello World"

# Check status
./start_bot.sh status

# View logs
./start_bot.sh logs

# Stop bot
./start_bot.sh stop
```

## Running as a System Service 🔧

For production use, you can run the bot as a systemd service:

```bash
# After running setup, install the service
sudo cp whatsapp-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable whatsapp-bot.service
sudo systemctl start whatsapp-bot.service

# Check service status
sudo systemctl status whatsapp-bot.service

# View service logs
sudo journalctl -u whatsapp-bot.service -f
```

## File Structure 📁

```
whatsapp-automation/
├── whatsapp_automation.py    # Main bot application
├── config.yaml              # Configuration file
├── setup.py                 # Setup script
├── start_bot.sh             # Launcher script
├── requirements.txt         # Python dependencies
├── whatsapp-bot.service     # Systemd service file
├── images/                  # Directory for image files
│   └── README.md           # Instructions for images
├── logs/                   # Log files directory
└── README.md               # This file
```

## Troubleshooting 🔧

### Common Issues

1. **"Browser not opening"**
   - Make sure you have a default browser set
   - Try running with GUI access (not SSH without X11 forwarding)

2. **"WhatsApp Web not logged in"**
   - Open WhatsApp Web manually and scan QR code
   - Keep the browser tab open

3. **"Phone number not found"**
   - Ensure phone numbers include country code (+1, +91, etc.)
   - Verify the contact exists in your WhatsApp

4. **"Group not found"**
   - Use the exact group name as it appears in WhatsApp
   - Ensure you're a member of the group

5. **"Image not sending"**
   - Check if image file exists
   - Verify image format is supported
   - Ensure image size is under 16MB

### Logs

Check the logs for detailed error information:

```bash
# View main log file
tail -f whatsapp_bot.log

# Using launcher script
./start_bot.sh logs
```

## Security & Privacy 🔒

- **Local Operation**: All processing happens locally on your machine
- **No Cloud Storage**: Messages and contacts are not stored in the cloud
- **WhatsApp Web**: Uses official WhatsApp Web interface
- **Configuration**: Keep your config.yaml file secure and private

## Limitations ⚠️

1. **WhatsApp Web Dependency**: Requires active WhatsApp Web session
2. **Browser Dependency**: Needs a graphical browser environment
3. **Rate Limiting**: WhatsApp may rate limit excessive messaging
4. **Group Images**: Limited support for sending images to groups
5. **Internet Connection**: Requires stable internet connection

## Contributing 🤝

Feel free to submit issues, feature requests, or pull requests to improve the bot!

## License 📄

This project is for educational and personal use. Please respect WhatsApp's Terms of Service and use responsibly.

## Support 💬

If you encounter issues:

1. Check the troubleshooting section
2. Review the logs for error messages
3. Ensure your configuration is correct
4. Verify WhatsApp Web is properly logged in

---

**Happy Automating! 🎉**
