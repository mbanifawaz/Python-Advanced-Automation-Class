This script is an automated news scraper that periodically fetches articles from BBC News and saves them in a JSON file. Below is a breakdown of how the script works and how it utilizes different Python libraries.

---

### **How the Script Works**
1. **Initialization (`__init__` method)**
   - Sets up request headers to mimic a real browser.
   - Defines the base URL for BBC News.
   - Creates an output directory to store the scraped data.

2. **Loading and Saving Data**
   - Loads previously scraped data from `scraped_news.json`.
   - Saves new data, ensuring only the last 100 articles are kept.

3. **Scraping News Articles (`scrape_news` method)**
   - Sends an HTTP GET request to BBC News using `requests`.
   - Parses the HTML response with `BeautifulSoup`.
   - Extracts details such as:
     - Title
     - Link
     - Description
     - Category
     - Last Updated Time
     - Image URL
   - Filters out duplicate articles.

4. **Scheduled Scraping (`start_scheduled_scraping` method)**
   - Runs the scraper every specified minutes using `schedule`.
   - Logs the time remaining until the next scrape.
   - Runs in a continuous loop until stopped by the user.

---

### **Libraries Used and Their Purpose**
1. **`requests`** - Fetches web pages (BBC News) via HTTP requests.
2. **`BeautifulSoup`** - Parses and extracts data from HTML content.
3. **`json`** - Saves and loads scraped news data.
4. **`datetime`** - Handles timestamps for logging and data storage.
5. **`schedule`** - Runs the scraping job at fixed time intervals.
6. **`time`** - Manages delays and scheduling in loops.
7. **`logging`** - Provides detailed logs for debugging and monitoring.
8. **`os`** - Manages file operations (creating directories and checking files).
9. **`threading`** - Runs a background thread to log time remaining before the next scrape.
10. **`urllib.parse.urljoin`** - Constructs absolute URLs from relative paths.

---

### **Key Features**
- **Automatic Data Collection:** Runs in the background, fetching news at set intervals.
- **Data Persistence:** Saves scraped news articles in a JSON file and prevents duplicates.
- **Logging & Error Handling:** Uses logging to track errors and system status.
- **Concurrency Support:** Uses threading to log time remaining until the next scrape.

This script is ideal for continuously monitoring news articles and keeping an up-to-date record in JSON format. 🚀