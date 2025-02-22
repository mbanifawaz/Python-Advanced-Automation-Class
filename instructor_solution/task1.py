import os
import time
import logging
from datetime import datetime
from pygtail import Pygtail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LogMonitor:
    def __init__(self, config_path='config.ini'):
        self.config = self._load_config(config_path)
        self.log_file = self.config['Monitoring']['log_file']
        self.offset_file = self.log_file + '.offset'
        self._setup_email_config()
        
    def _load_config(self, config_path):
        """Load configuration from ini file"""
        if not os.path.exists(config_path):
            self._create_default_config(config_path)
            
        config = ConfigParser()
        config.read(config_path)
        return config
    
    def _create_default_config(self, config_path):
        """Create default configuration file"""
        config = ConfigParser()
        config['Email'] = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': '587',
            'sender_email': 'your-email@gmail.com',
            'sender_password': 'your-app-password',  # Use App Password for Gmail
            'recipient_email': 'recipient@example.com'
        }
        config['Monitoring'] = {
            'log_file': 'sample.log',
            'check_interval': '5'  # seconds
        }
        
        with open(config_path, 'w') as f:
            config.write(f)
        
        logging.info(f"Created default configuration file at {config_path}")
        
    def _setup_email_config(self):
        """Setup email configuration from config file"""
        email_config = self.config['Email']
        self.smtp_server = email_config['smtp_server']
        self.smtp_port = int(email_config['smtp_port'])
        self.sender_email = email_config['sender_email']
        self.sender_password = email_config['sender_password']
        self.recipient_email = email_config['recipient_email']
    
    def send_email_alert(self, error_message, timestamp):
        """Send email alert for critical errors"""
        try:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.recipient_email
            message["Subject"] = "CRITICAL ERROR Alert"
            
            body = f"""
            Critical Error Detected!
            
            Timestamp: {timestamp}
            Error Message: {error_message}
            
            This is an automated alert from your Log Monitoring System.
            """
            
            message.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
                
            logging.info("Email alert sent successfully")
            
        except Exception as e:
            logging.error(f"Failed to send email alert: {str(e)}")
    
    def create_sample_log(self):
        """Create a sample log file if it doesn't exist"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write(f"{datetime.now()} - INFO - System startup\n")
            logging.info(f"Created sample log file: {self.log_file}")
    
    def monitor_log(self):
        """Monitor log file for critical errors"""
        self.create_sample_log()
        
        logging.info(f"Starting to monitor log file: {self.log_file}")
        
        while True:
            try:
                # Use pygtail to read only new lines
                for line in Pygtail(self.log_file):
                    if "CRITICAL ERROR" in line:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        logging.warning(f"Critical error detected: {line.strip()}")
                        self.send_email_alert(line.strip(), timestamp)
                
                # Wait before checking for new lines
                time.sleep(int(self.config['Monitoring']['check_interval']))
                
            except Exception as e:
                logging.error(f"Error monitoring log file: {str(e)}")
                time.sleep(5)  # Wait before retrying

def main():
    try:
        monitor = LogMonitor()
        monitor.monitor_log()
    except KeyboardInterrupt:
        logging.info("Log monitoring stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()