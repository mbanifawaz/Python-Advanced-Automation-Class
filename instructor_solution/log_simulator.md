from flask import Flask, render_template, redirect, url_for
import logging
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create file and console handlers
file_handler = logging.FileHandler('sample.log')
console_handler = logging.StreamHandler()

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_normal(message):
    logger.info(message)
    return redirect(url_for('home'))

def log_error(message):
    logger.error(message)
    return redirect(url_for('home'))

def log_critical(message):
    logger.critical(message)
    return redirect(url_for('home'))

def read_log_file():
    try:
        with open('sample.log', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return 'No log file found.'

@app.route('/')
def home():
    log_contents = read_log_file()
    return render_template('index.html', log_contents=log_contents)

@app.route('/log_normal')
def log_normal_route():
    log_normal('Normal activity logged.')
    return redirect(url_for('home'))

@app.route('/log_error')
def log_error_route():
    log_error('Error logged.')
    return redirect(url_for('home'))

@app.route('/log_critical')
def log_critical_route():
    log_critical('Critical error logged.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()from flask import Flask, render_template, redirect, url_for
import logging
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('sample.log'),
        logging.StreamHandler()
    ]
)

# Define logging functions
def log_normal(message):
    logging.info(message)
    return redirect(url_for('home'))

def log_error(message):
    logging.warning(message)
    return redirect(url_for('home'))

def log_critical(message):
    logging.error(message)
    return redirect(url_for('home'))

# Function to read log file
def read_log_file():
    try:
        with open('sample.log', 'r') as file:
            log_contents = file.read()
            return log_contents
    except FileNotFoundError:
        return 'Log file not found.'

# Define routes
@app.route('/')
def home():
    log_contents = read_log_file()
    return render_template('index.html', log_contents=log_contents)

@app.route('/log_normal')
def log_normal_activity():
    log_normal('Normal activity logged.')
    return redirect(url_for('home'))

@app.route('/log_error')
def log_error_activity():
    log_error('Error logged.')
    return redirect(url_for('home'))

@app.route('/log_critical')
def log_critical_activity():
    log_critical('Critical error logged.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()This Flask web application acts as a **log simulator**, allowing users to generate and view logs through a simple web interface. Below is an overview of its functionality and the key components.

---

### **How the Script Works**
1. **Flask Web Server (`app = Flask(__name__)`)**
   - Initializes a Flask app to serve a simple web interface.
   - Runs the app in debug mode for development.

2. **Logging Configuration (`logging.basicConfig`)**
   - Logs messages to both the console and a file (`sample.log`).
   - Supports three levels of logging:
     - **INFO**: Normal activities.
     - **WARNING**: Errors.
     - **ERROR**: Critical failures.

3. **HTML User Interface**
   - Uses **Bootstrap** for styling.
   - Displays buttons for generating different types of log messages.
   - Shows the contents of the log file dynamically.

4. **Logging Functions**
   - **`log_normal()`**: Logs normal activity.
   - **`log_error()`**: Logs an error message.
   - **`log_critical()`**: Logs a critical error.
   - Each function appends a timestamped message to `sample.log` and redirects back to the home page.

5. **Reading Log Files (`read_log_file()`)**
   - Fetches log contents to display on the webpage.
   - Returns a default message if the log file doesn’t exist.

---

### **Libraries Used and Their Purpose**
1. **`Flask`** - Web framework to handle routing and rendering.
2. **`logging`** - Writes and manages log messages.
3. **`datetime`** - Adds timestamps to log entries.

---

### **Key Features**
- **Interactive Logging**: Users can generate logs with a single click.
- **Real-Time Log Viewing**: Displays log file contents dynamically.
- **Bootstrap Styling**: Provides a clean and responsive UI.
- **File-Based Logging**: Stores logs persistently in `sample.log`.

This script is a simple yet effective way to simulate and manage logging within a web application. 🚀