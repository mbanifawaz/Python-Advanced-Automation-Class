**Advanced Python Automation Tasks**

**Instructor's LinkedIn Profile:**
   - [Munes Bani Fawaz LinkedIn](https://www.linkedin.com/in/munes-bani-fawaz-799151204/)

**Lecture Video:**
   - [Download the Lecture Video](https://github.com/mbanifawaz/Python-Advanced-Automation-Class/blob/main/Lecture.mp4)

## **Task 1: Log Monitoring & Email Alert System**

### **Objective:**
- Automate log file monitoring in real-time and send an email alert when a critical error appears.

### **Instructions:**
1. **Monitor a Log File in Real-Time:**
   - Write a Python script to continuously read a log file as new lines are added.
   - Detect lines containing the text `CRITICAL ERROR`.
   - Ensure compatibility across Windows and Ubuntu.
   - Use `pygtail` for cross-platform file monitoring.

2. **Send an Email Alert:**
   - If a `CRITICAL ERROR` appears, automatically send an email notification.
   - The email should contain the error message and timestamp.

3. **Use SMTP for Emailing:**
   - Use Python’s `smtplib` and `email.mime` to send an email.
   - You can use Gmail SMTP or another mail provider.

4. **Test Your Script:**
   - Generate a sample log file (`sample.log`) with different log levels (`INFO`, `WARNING`, `ERROR`, `CRITICAL ERROR`).
   - Append new log lines to test real-time monitoring.

### **Requirements:**
- Use `smtplib` for sending emails.
- Use `pygtail` for real-time monitoring (cross-platform for Windows & Ubuntu).
- Ensure the script runs on both Windows and Ubuntu.
- Handle errors properly.

### **Expected Output:**
- If a `CRITICAL ERROR` is detected, an email should be sent with the log details.
- The script should continuously monitor the log file without stopping.

---

## **Task 2: Web Scraping & Data Automation**

### **Objective:**
- Automate data extraction from a website and store it in a structured format.

### **Instructions:**
1. **Select a Public Website:**
   - Choose a website that displays structured data (e.g., news headlines, weather data, stock prices).

2. **Scrape Data Using `BeautifulSoup` or `Scrapy`:**
   - Extract relevant information such as:
     - News headlines (if scraping a news site).
     - Temperature and weather conditions (if scraping a weather site).
     - Stock prices (if scraping a financial site).
   - Ensure the script runs on both Windows and Ubuntu.

3. **Store the Extracted Data:**
   - Save the data into a JSON file using Python’s `json` module.

4. **Automate the Scraping Process:**
   - Use `schedule` or `APScheduler` to run the script automatically at a set interval (e.g., every hour).

### **Requirements:**
- Use `requests` and `BeautifulSoup` or `Scrapy` for scraping.
- Save data into a JSON file.
- Automate execution using `schedule`.
- Ensure compatibility with both Windows and Ubuntu.
- Handle exceptions for failed requests.

### **Expected Output:**
- The script should extract and store data periodically.
- The JSON file should contain the scraped information with timestamps.

---

## **Setup Guide for Windows & Ubuntu**

### **Installing Python & IDEs**

#### **For Windows:**
1. **Install Python:**
   - Download Python from [official website](https://www.python.org/downloads/).
   - Run the installer and check the box **“Add Python to PATH”** before installing.
   - Verify installation by running `python --version` in Command Prompt.

2. **Install VS Code:**
   - Download VS Code from [official website](https://code.visualstudio.com/).
   - Install Python extension from the Extensions Marketplace.

3. **Install PyCharm:**
   - Download PyCharm Community Edition from [JetBrains](https://www.jetbrains.com/pycharm/download/).
   - Follow the installation steps and launch PyCharm.

#### **For Ubuntu:**
1. **Install VS Code:**
   - Open a terminal and run:
     ```sh
     sudo apt update && sudo apt install code
     ```

2. **Install PyCharm:**
   - Download PyCharm from [JetBrains](https://www.jetbrains.com/pycharm/download/).
   - Run the installer and follow the instructions.

---

### **Submission Guidelines:**
- Submit the full Python scripts for both tasks.
- Provide a short README file explaining how your scripts work.
- Include sample log files and output JSON files.
- Ensure that the scripts run on both Windows and Ubuntu.

Good luck! 🚀

