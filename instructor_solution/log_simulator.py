from flask import Flask, render_template_string, request, redirect, url_for
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Path to the log file
LOG_FILE = 'sample.log'

# HTML template with Bootstrap for styling
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Log Simulator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            padding: 20px;
            background-color: #f8f9fa;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        .log-container {
            margin-top: 20px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .btn {
            margin: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Log Simulator</h1>
        <div class="text-center">
            <form action="/log_normal" method="post">
                <button type="submit" class="btn btn-success">Log Normal Activity</button>
            </form>
            <form action="/log_error" method="post">
                <button type="submit" class="btn btn-warning">Log Error</button>
            </form>
            <form action="/log_critical" method="post">
                <button type="submit" class="btn btn-danger">Log Critical Error</button>
            </form>
        </div>
        <div class="log-container">
            <h3>Log File Content</h3>
            <pre>{{ log_content }}</pre>
        </div>
    </div>
</body>
</html>
'''

def read_log_file():
    """Read the content of the log file."""
    try:
        with open(LOG_FILE, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Log file is empty or does not exist."

@app.route('/')
def index():
    """Render the main page with buttons and log file content."""
    log_content = read_log_file()
    return render_template_string(HTML_TEMPLATE, log_content=log_content)

@app.route('/log_normal', methods=['POST'])
def log_normal():
    """Log normal activity and redirect to home page."""
    log_message = f"{datetime.now()} - INFO - Normal activity"
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + '\n')
    logging.info("Logged normal activity")
    return redirect(url_for('index'))

@app.route('/log_error', methods=['POST'])
def log_error():
    """Log an error and redirect to home page."""
    log_message = f"{datetime.now()} - ERROR - An error occurred"
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + '\n')
    logging.warning("Logged error")
    return redirect(url_for('index'))

@app.route('/log_critical', methods=['POST'])
def log_critical():
    """Log a critical error and redirect to home page."""
    log_message = f"{datetime.now()} - CRITICAL ERROR - A critical error occurred"
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + '\n')
    logging.error("Logged critical error")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)