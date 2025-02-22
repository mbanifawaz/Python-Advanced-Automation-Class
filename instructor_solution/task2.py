import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import schedule
import time
import logging
import os
from typing import Dict, List, Any
from urllib.parse import urljoin
import threading

# Configure logging with more detail
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class NewsScraperAutomation:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        self.base_url = 'https://www.bbc.com/news'
        self.output_file = 'scraped_news.json'
        self.create_output_dir()

    def create_output_dir(self) -> None:
        """Create output directory if it doesn't exist"""
        os.makedirs('output', exist_ok=True)
        self.output_file = os.path.join('output', self.output_file)

    def load_existing_data(self) -> List[Dict[str, Any]]:
        """Load existing scraped data from JSON file"""
        try:
            if os.path.exists(self.output_file):
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Error loading existing data: {str(e)}")
        return []

    def save_data(self, data: List[Dict[str, Any]]) -> None:
        """Save scraped data to JSON file"""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logging.info(f"Data successfully saved to {self.output_file}")
        except Exception as e:
            logging.error(f"Error saving data: {str(e)}")

    def scrape_news(self) -> List[Dict[str, Any]]:
        """Scrape news articles from BBC News"""
        try:
            logging.debug(f"Attempting to fetch {self.base_url}")
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            logging.debug(f"Successfully got response with status code: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all article cards using the new structure
            articles = soup.find_all('div', {'data-testid': lambda x: x and 'card' in x.lower()})
            
            logging.debug(f"Found {len(articles)} potential articles")
            
            scraped_data = []
            for article in articles:
                try:
                    # Find the article link
                    link_elem = article.find('a', {'data-testid': 'internal-link'})
                    if not link_elem:
                        continue
                    
                    # Get the link
                    link = link_elem.get('href', '')
                    if link:
                        link = urljoin(self.base_url, link)
                    
                    # Get the headline
                    headline_elem = article.find('h2', {'data-testid': 'card-headline'})
                    if not headline_elem:
                        continue
                    title = headline_elem.get_text().strip()
                    
                    # Get the description
                    description = ''
                    desc_elem = article.find('p', {'data-testid': 'card-description'})
                    if desc_elem:
                        description = desc_elem.get_text().strip()
                    
                    # Get the category/tag
                    category = ''
                    category_elem = article.find('span', {'data-testid': 'card-metadata-tag'})
                    if category_elem:
                        category = category_elem.get_text().strip()
                    
                    # Get the last updated time
                    last_updated = ''
                    time_elem = article.find('span', {'data-testid': 'card-metadata-lastupdated'})
                    if time_elem:
                        last_updated = time_elem.get_text().strip()
                    
                    # Get the image URL if available
                    image_url = ''
                    img_elem = article.find('img')
                    if img_elem:
                        image_url = img_elem.get('src', '')
                        # Get the highest resolution from srcset if available
                        srcset = img_elem.get('srcset', '')
                        if srcset:
                            # Get the last (highest resolution) image from srcset
                            highest_res = srcset.split(',')[-1].split()[0]
                            if highest_res:
                                image_url = highest_res
                    
                    article_data = {
                        'title': title,
                        'link': link,
                        'description': description,
                        'category': category,
                        'last_updated': last_updated,
                        'image_url': image_url,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    scraped_data.append(article_data)
                    logging.debug(f"Scraped article: {title}")
                    
                except Exception as e:
                    logging.error(f"Error processing article: {str(e)}")
                    continue
            
            logging.info(f"Successfully scraped {len(scraped_data)} articles")
            return scraped_data
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {str(e)}")
            return []
        except Exception as e:
            logging.error(f"Unexpected error during scraping: {str(e)}")
            return []

    def update_data(self) -> None:
        """Update scraped data and save to JSON file"""
        try:
            logging.info("Starting scraping process...")
            
            # Load existing data
            existing_data = self.load_existing_data()
            
            # Get new data
            new_data = self.scrape_news()
            
            if new_data:
                # Remove duplicates based on title
                seen_titles = set(item['title'] for item in existing_data)
                unique_new_data = [
                    item for item in new_data 
                    if item['title'] not in seen_titles
                ]
                
                # Combine existing and new data
                all_data = existing_data + unique_new_data
                
                # Keep only the last 100 entries to manage file size
                all_data = all_data[-100:]
                
                # Save updated data
                self.save_data(all_data)
                logging.info(f"Successfully scraped and saved {len(unique_new_data)} new articles")
            else:
                logging.warning("No new data scraped")
                
        except Exception as e:
            logging.error(f"Error in update process: {str(e)}")

    def start_scheduled_scraping(self, interval_minutes: int = 1) -> None:
        """Start scheduled scraping at specified interval"""
        logging.info(f"Starting scheduled scraping every {interval_minutes} minutes")
        
        # Do initial scrape
        self.update_data()
        
        # Schedule the scraping task
        schedule.every(interval_minutes).minutes.do(self.update_data)
        
        # Function to log time remaining until next scrape
        def log_time_remaining():
            while True:
                next_run = schedule.next_run()
                time_remaining = next_run - datetime.now()
                logging.info(f"Time remaining until next scrape: {time_remaining}")
                time.sleep(1)  # Log every 1 seconds

        # Start the logging function in a separate thread
        threading.Thread(target=log_time_remaining, daemon=True).start()
        
        # Keep the script running
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                logging.info("Scraping stopped by user")
                break
            except Exception as e:
                logging.error(f"Error in scheduling: {str(e)}")
                time.sleep(1)  # Wait a minute before retrying

def main():
    """Main function to start the scraper"""
    try:
        scraper = NewsScraperAutomation()
        # Start scraping every 1 minutes
        scraper.start_scheduled_scraping(interval_minutes=1)
    except KeyboardInterrupt:
        logging.info("Program terminated by user")
    except Exception as e:
        logging.error(f"Program error: {str(e)}")

if __name__ == "__main__":
    main()