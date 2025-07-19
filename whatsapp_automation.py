#!/usr/bin/env python3
"""
WhatsApp Automation Bot
Sends scheduled messages to groups and personal contacts
Supports text messages, images with/without captions
"""

import pywhatkit as kit
import schedule
import time
import yaml
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('whatsapp_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class WhatsAppBot:
    def __init__(self, config_file: str = "config.yaml"):
        """Initialize the WhatsApp automation bot."""
        self.config_file = config_file
        self.config = self.load_config()
        self.scheduled_jobs = []
        logger.info("WhatsApp Bot initialized successfully")
    
    def load_config(self) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                logger.info(f"Configuration loaded from {self.config_file}")
                return config
        except FileNotFoundError:
            logger.error(f"Configuration file {self.config_file} not found")
            self.create_sample_config()
            return {}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML configuration: {e}")
            return {}
    
    def create_sample_config(self):
        """Create a sample configuration file."""
        sample_config = {
            'contacts': {
                'personal': [
                    {
                        'name': 'John Doe',
                        'phone': '+1234567890',
                        'messages': [
                            {
                                'type': 'text',
                                'content': 'Good morning! Have a great day!',
                                'time': '09:00'
                            }
                        ]
                    }
                ],
                'groups': [
                    {
                        'name': 'Family Group',
                        'messages': [
                            {
                                'type': 'text',
                                'content': 'Good morning everyone!',
                                'time': '08:30'
                            },
                            {
                                'type': 'image',
                                'image_path': 'images/motivational_quote.jpg',
                                'caption': 'Daily motivation!',
                                'time': '18:00'
                            }
                        ]
                    }
                ]
            },
            'settings': {
                'wait_time': 20,  # seconds to wait after opening WhatsApp
                'close_tab': True,  # close tab after sending message
                'image_formats': ['.jpg', '.jpeg', '.png', '.gif'],
                'timezone': 'local'
            }
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as file:
            yaml.dump(sample_config, file, default_flow_style=False, allow_unicode=True)
        
        logger.info(f"Sample configuration created at {self.config_file}")
        print(f"Please edit {self.config_file} with your contacts and messages")
    
    def validate_phone_number(self, phone: str) -> str:
        """Validate and format phone number."""
        # Remove spaces and special characters except +
        phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # Ensure phone starts with country code
        if not phone.startswith('+'):
            logger.warning(f"Phone number {phone} doesn't start with country code (+)")
            return phone
        
        return phone
    
    def validate_image_path(self, image_path: str) -> bool:
        """Validate if image file exists and is in supported format."""
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return False
        
        supported_formats = self.config.get('settings', {}).get('image_formats', ['.jpg', '.jpeg', '.png', '.gif'])
        file_extension = os.path.splitext(image_path)[1].lower()
        
        if file_extension not in supported_formats:
            logger.error(f"Unsupported image format: {file_extension}")
            return False
        
        return True
    
    def send_text_message(self, phone: str, message: str, contact_name: str = "Unknown"):
        """Send a text message to a phone number."""
        try:
            phone = self.validate_phone_number(phone)
            wait_time = self.config.get('settings', {}).get('wait_time', 20)
            close_tab = self.config.get('settings', {}).get('close_tab', True)
            
            logger.info(f"Sending text message to {contact_name} ({phone})")
            
            # Send message immediately
            kit.sendwhatmsg_instantly(
                phone_no=phone,
                message=message,
                wait_time=wait_time,
                tab_close=close_tab
            )
            
            logger.info(f"Text message sent successfully to {contact_name}")
            
        except Exception as e:
            logger.error(f"Failed to send text message to {contact_name}: {str(e)}")
    
    def send_image_message(self, phone: str, image_path: str, caption: str = "", contact_name: str = "Unknown"):
        """Send an image message to a phone number."""
        try:
            if not self.validate_image_path(image_path):
                return
            
            phone = self.validate_phone_number(phone)
            wait_time = self.config.get('settings', {}).get('wait_time', 20)
            close_tab = self.config.get('settings', {}).get('close_tab', True)
            
            logger.info(f"Sending image to {contact_name} ({phone})")
            
            if caption:
                kit.sendwhats_image(
                    receiver=phone,
                    img_path=image_path,
                    caption=caption,
                    wait_time=wait_time,
                    tab_close=close_tab
                )
                logger.info(f"Image with caption sent successfully to {contact_name}")
            else:
                kit.sendwhats_image(
                    receiver=phone,
                    img_path=image_path,
                    wait_time=wait_time,
                    tab_close=close_tab
                )
                logger.info(f"Image sent successfully to {contact_name}")
                
        except Exception as e:
            logger.error(f"Failed to send image to {contact_name}: {str(e)}")
    
    def send_group_message(self, group_name: str, message: str):
        """Send a text message to a WhatsApp group."""
        try:
            wait_time = self.config.get('settings', {}).get('wait_time', 20)
            close_tab = self.config.get('settings', {}).get('close_tab', True)
            
            logger.info(f"Sending text message to group: {group_name}")
            
            kit.sendwhatmsg_to_group_instantly(
                group_id=group_name,
                message=message,
                wait_time=wait_time,
                tab_close=close_tab
            )
            
            logger.info(f"Text message sent successfully to group: {group_name}")
            
        except Exception as e:
            logger.error(f"Failed to send message to group {group_name}: {str(e)}")
    
    def process_message(self, contact_info: Dict, message_info: Dict, is_group: bool = False):
        """Process and send a single message."""
        try:
            message_type = message_info.get('type', 'text')
            
            if is_group:
                contact_identifier = contact_info.get('name', 'Unknown Group')
                if message_type == 'text':
                    content = message_info.get('content', '')
                    self.send_group_message(contact_identifier, content)
                elif message_type == 'image':
                    # For groups, we'll use individual phone numbers if available
                    # or log that group image sending is limited
                    logger.warning(f"Image sending to groups is limited. Consider sending to individual members.")
            else:
                phone = contact_info.get('phone', '')
                contact_name = contact_info.get('name', 'Unknown')
                
                if message_type == 'text':
                    content = message_info.get('content', '')
                    self.send_text_message(phone, content, contact_name)
                elif message_type == 'image':
                    image_path = message_info.get('image_path', '')
                    caption = message_info.get('caption', '')
                    self.send_image_message(phone, image_path, caption, contact_name)
                    
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
    
    def schedule_messages(self):
        """Schedule all messages based on configuration."""
        if not self.config:
            logger.error("No configuration loaded. Cannot schedule messages.")
            return
        
        contacts = self.config.get('contacts', {})
        
        # Schedule personal contact messages
        personal_contacts = contacts.get('personal', [])
        for contact in personal_contacts:
            messages = contact.get('messages', [])
            for message in messages:
                time_str = message.get('time', '')
                if time_str:
                    schedule.every().day.at(time_str).do(
                        self.process_message, contact, message, False
                    )
                    logger.info(f"Scheduled message for {contact.get('name', 'Unknown')} at {time_str}")
        
        # Schedule group messages
        groups = contacts.get('groups', [])
        for group in groups:
            messages = group.get('messages', [])
            for message in messages:
                time_str = message.get('time', '')
                if time_str:
                    schedule.every().day.at(time_str).do(
                        self.process_message, group, message, True
                    )
                    logger.info(f"Scheduled message for group {group.get('name', 'Unknown')} at {time_str}")
    
    def run_scheduler(self):
        """Run the message scheduler."""
        logger.info("WhatsApp Bot scheduler started")
        
        if not self.config:
            logger.error("No configuration found. Exiting.")
            return
        
        self.schedule_messages()
        
        logger.info("All messages scheduled successfully")
        print("WhatsApp Bot is running... Press Ctrl+C to stop")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("WhatsApp Bot stopped by user")
            print("\nWhatsApp Bot stopped.")
    
    def send_test_message(self, phone: str, message: str = "Test message from WhatsApp Bot"):
        """Send a test message to verify setup."""
        logger.info("Sending test message...")
        self.send_text_message(phone, message, "Test Contact")
    
    def list_scheduled_jobs(self):
        """List all scheduled jobs."""
        jobs = schedule.jobs
        if not jobs:
            print("No jobs scheduled.")
            return
        
        print("Scheduled Jobs:")
        for i, job in enumerate(jobs, 1):
            print(f"{i}. {job}")

def main():
    """Main function to run the WhatsApp bot."""
    bot = WhatsAppBot()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test" and len(sys.argv) > 2:
            phone = sys.argv[2]
            message = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else "Test message"
            bot.send_test_message(phone, message)
        elif command == "schedule":
            bot.list_scheduled_jobs()
        elif command == "run":
            bot.run_scheduler()
        else:
            print("Usage:")
            print("  python whatsapp_automation.py run              - Start the scheduler")
            print("  python whatsapp_automation.py test <phone>     - Send test message")
            print("  python whatsapp_automation.py schedule         - List scheduled jobs")
    else:
        bot.run_scheduler()

if __name__ == "__main__":
    main()