#!/usr/bin/env python3
"""
Setup script for WhatsApp Automation Bot
Installs dependencies and sets up the environment
"""

import subprocess
import sys
import os
import shutil

def run_command(command):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def install_dependencies():
    """Install required Python packages."""
    print("Installing Python dependencies...")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print("Creating virtual environment...")
        venv_path = "venv"
        
        # Create virtual environment
        success, output = run_command(f"{sys.executable} -m venv {venv_path}")
        if not success:
            print(f"Failed to create virtual environment: {output}")
            print("Trying with --break-system-packages flag...")
            success, output = run_command(f"{sys.executable} -m pip install -r requirements.txt --break-system-packages")
            if success:
                print("✅ Dependencies installed successfully!")
                return True
            else:
                print(f"❌ Failed to install dependencies: {output}")
                return False
        
        # Use virtual environment python and pip
        if os.name == 'nt':  # Windows
            python_exe = os.path.join(venv_path, "Scripts", "python.exe")
            pip_exe = os.path.join(venv_path, "Scripts", "pip.exe")
        else:  # Unix/Linux/macOS
            python_exe = os.path.join(venv_path, "bin", "python")
            pip_exe = os.path.join(venv_path, "bin", "pip")
        
        print(f"✅ Virtual environment created at: {venv_path}")
        print("Installing dependencies in virtual environment...")
        
        # Upgrade pip in venv
        success, output = run_command(f"{pip_exe} install --upgrade pip")
        if not success:
            print(f"Warning: Failed to upgrade pip in venv: {output}")
        
        # Install requirements in venv
        success, output = run_command(f"{pip_exe} install -r requirements.txt")
        if success:
            print("✅ Dependencies installed successfully in virtual environment!")
            
            # Create activation script
            create_venv_activation_script(venv_path)
            return True
        else:
            print(f"❌ Failed to install dependencies in venv: {output}")
            return False
    else:
        # We're already in a virtual environment
        # Upgrade pip first
        success, output = run_command(f"{sys.executable} -m pip install --upgrade pip")
        if not success:
            print(f"Warning: Failed to upgrade pip: {output}")
        
        # Install requirements
        success, output = run_command(f"{sys.executable} -m pip install -r requirements.txt")
        if success:
            print("✅ Dependencies installed successfully!")
            return True
        else:
            print(f"❌ Failed to install dependencies: {output}")
            return False

def create_directories():
    """Create necessary directories."""
    directories = ["images", "logs"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def create_service_file():
    """Create a systemd service file for running the bot in background."""
    service_content = f"""[Unit]
Description=WhatsApp Automation Bot
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'ubuntu')}
WorkingDirectory={os.getcwd()}
ExecStart={sys.executable} {os.path.join(os.getcwd(), 'whatsapp_automation.py')} run
Restart=always
RestartSec=10
Environment=DISPLAY=:0
Environment=PYTHONPATH={os.getcwd()}

[Install]
WantedBy=multi-user.target
"""
    
    service_file = "whatsapp-bot.service"
    with open(service_file, 'w') as f:
        f.write(service_content)
    
    print(f"✅ Created service file: {service_file}")
    print(f"To install as system service, run:")
    print(f"sudo cp {service_file} /etc/systemd/system/")
    print(f"sudo systemctl enable whatsapp-bot.service")
    print(f"sudo systemctl start whatsapp-bot.service")

def create_venv_activation_script(venv_path):
    """Create activation script for the virtual environment."""
    if os.name == 'nt':  # Windows
        python_exe = os.path.join(venv_path, "Scripts", "python.exe")
    else:  # Unix/Linux/macOS
        python_exe = os.path.join(venv_path, "bin", "python")
    
    activation_script = f"""#!/bin/bash
# WhatsApp Bot Virtual Environment Activation
# Source this file to activate the virtual environment

# Activate virtual environment
source {venv_path}/bin/activate

echo "Virtual environment activated!"
echo "Python executable: {python_exe}"
echo ""
echo "You can now run:"
echo "  python whatsapp_automation.py run"
echo "  python whatsapp_automation.py test +1234567890"
echo ""
echo "Or use the launcher script:"
echo "  ./start_bot.sh run"
"""
    
    with open("activate_venv.sh", "w") as f:
        f.write(activation_script)
    
    # Make it executable
    run_command("chmod +x activate_venv.sh")
    print("✅ Created virtual environment activation script: activate_venv.sh")

def setup_sample_images():
    """Create sample images directory with instructions."""
    images_dir = "images"
    readme_content = """# Images Directory

Place your image files here that you want to send via WhatsApp.

Supported formats:
- .jpg / .jpeg
- .png
- .gif
- .webp

Example usage in config.yaml:
```yaml
- type: "image"
  image_path: "images/your_image.jpg"
  caption: "Optional caption text"
  time: "09:00"
```

Note: Make sure your images are not too large (< 16MB) for WhatsApp compatibility.
"""
    
    readme_path = os.path.join(images_dir, "README.md")
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Created images directory with instructions")

def main():
    """Main setup function."""
    print("🚀 Setting up WhatsApp Automation Bot...")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed due to dependency installation errors.")
        sys.exit(1)
    
    # Setup sample images directory
    setup_sample_images()
    
    # Create service file
    create_service_file()
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit config.yaml with your contacts and messages")
    print("2. Add images to the 'images' directory if needed")
    print("3. Test the bot with: python whatsapp_automation.py test +1234567890")
    print("4. Run the bot with: python whatsapp_automation.py run")
    print("5. For background service, follow the systemd instructions above")
    print("\n⚠️  Important: Make sure WhatsApp Web is logged in on your default browser!")

if __name__ == "__main__":
    main()