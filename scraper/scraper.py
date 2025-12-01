"""
Main scraper class - Core scraping logic
"""
import os
import csv
import time
import re
from datetime import datetime, timedelta
from typing import Dict, Set

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

from config import CSV_FILENAME, CSV_ENCODING, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT, USER_AGENT
from config import SCROLL_ATTEMPTS_CONTAINER, SCROLL_ATTEMPTS_WINDOW, SCROLL_DELAY, DELAY_BETWEEN_LOCATIONS, PROCESSING_DELAY
from language_dict import DATE_PATTERNS, COOKIE_SELECTORS, REVIEW_BUTTONS, CONTAINER_SELECTORS, REVIEW_SELECTORS


class UnifiedReviewScraper:
    def __init__(self, csv_filename=CSV_FILENAME):
        """Initialize the unified scraper for all sources"""
        # Ensure data directory exists
        os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
        
        self.csv_filename = csv_filename
        self.initialize_csv()
        
    def setup_driver(self):
        """Setup Chrome driver with performance optimizations"""
        chrome_options = Options()
        
        # Performance optimizations
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('prefs', {
            'profile.default_content_setting_values.notifications': 2,
            'profile.managed_default_content_settings.images': 2,
        })
        chrome_options.add_argument(f"--user-agent={USER_AGENT}")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        
    def initialize_csv(self):
        """Initialize CSV file if it doesn't exist"""
        if not os.path.exists(self.csv_filename):
            with open(self.csv_filename, 'w', newline='', encoding=CSV_ENCODING) as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'name', 'source', 'location', 'date', 'rating', 'comment'])
    
    def save_review(self, review):
        """Save a review to CSV with duplicate checking"""
        try:
            # Read existing IDs
            existing_ids = set()
            if os.path.exists(self.csv_filename):
                with open(self.csv_filename, 'r', encoding=CSV_ENCODING) as f:
                    reader = csv.reader(f)
                    next(reader, None)
                    for row in reader:
                        if row:
                            existing_ids.add(row[0])
            
            # Check for duplicate
            if review['id'] in existing_ids:
                return False
            
            # Append to CSV
            with open(self.csv_filename, 'a', newline='', encoding=CSV_ENCODING) as f:
                writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                writer.writerow([
                    review['id'],
                    review['name'],
                    review['source'],
                    review['location'],
                    review['date'],
                    review['rating'],
                    review['comment']
                ])
            return True
            
        except Exception as e:
            return False
    
    # ========== GOOGLE MAPS SCRAPING ==========
    
    def accept_cookies(self):
        """Handle cookie consent quickly"""
        try:
            for selector in COOKIE_SELECTORS:
                try:
                    button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    button.click()
                    time.sleep(1)
                    return True
                except:
                    continue
        except:
            pass
        return False
    
    def ensure_reviews_tab_open(self):
        """Ensure we're on the reviews tab"""
        try:
            time.sleep(2)
            
            # Check if we're already on reviews
            try:
                reviews = self.driver.find_elements(By.XPATH, '//div[contains(@class, "jftiEf")]')
                if reviews:
                    return True
            except:
                pass
            
            # Try to click reviews button
            for button_xpath in REVIEW_BUTTONS:
                try:
                    button = self.wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                    button.click()
                    time.sleep(3)
                    return True
                except:
                    continue
                    
            # JavaScript fallback
            self.driver.execute_script("""
                var buttons = document.querySelectorAll('button');
                for (var btn of buttons) {
                    var text = btn.textContent || btn.innerText || '';
                    var aria = btn.getAttribute('aria-label') || '';
                    if (text.toLowerCase().includes('review') || 
                        text.toLowerCase().includes('avis') || 
                        aria.toLowerCase().includes('review')) {
                        btn.click();
                        return true;
                    }
                }
                return false;
            """)
            time.sleep(3)
            return True
            
        except Exception as e:
            return False
    
    def find_scrollable_container(self):
        """Find the scrollable reviews container"""
        for selector in CONTAINER_SELECTORS:
            try:
                container = self.driver.find_element(By.XPATH, selector)
                return container
            except:
                continue
        
        return None
    
    def scroll_to_load_reviews(self):
        """Scroll to load all available reviews"""
        container = self.find_scrollable_container()
        
        if container:
            # Scroll specific container
            last_height = self.driver.execute_script("return arguments[0].scrollHeight", container)
            scroll_attempts = 0
            
            while scroll_attempts < SCROLL_ATTEMPTS_CONTAINER:
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', container)
                time.sleep(SCROLL_DELAY)
                
                new_height = self.driver.execute_script("return arguments[0].scrollHeight", container)
                
                if new_height == last_height:
                    break
                
                last_height = new_height
                scroll_attempts += 1
        else:
            # Scroll entire window
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            
            while scroll_attempts < SCROLL_ATTEMPTS_WINDOW:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_DELAY)
                
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    break
                
                last_height = new_height
                scroll_attempts += 1
        
        time.sleep(2)
        return True
    
    def get_review_elements_google(self):
        """Find all review elements on Google Maps page"""
        for selector in REVIEW_SELECTORS:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                if elements:
                    return elements
            except:
                continue
        
        # Fallback
        try:
            elements = self.driver.find_elements(By.XPATH, '//span[@class="wiI7pd"]/ancestor::div[1]')
            if elements:
                return elements
        except:
            pass
        
        return []
    
    def extract_google_review_data(self, element, location_name):
        """Extract data from a Google Maps review element"""
        try:
            # NAME
            name = "Anonymous"
            try:
                name_elem = element.find_element(By.XPATH, './/div[contains(@class, "d4r55")]')
                name = name_elem.text.strip()
            except:
                pass
            
            # RATING
            rating = 0
            try:
                rating_elem = element.find_element(By.XPATH, './/span[@class="kvMYJc"]')
                aria_label = rating_elem.get_attribute("aria-label")
                if aria_label:
                    match = re.search(r'(\d+(?:\.\d+)?)', aria_label)
                    if match:
                        rating = int(float(match.group(1)))
            except:
                pass
            
            # DATE
            date_text = "N/A"
            try:
                date_elem = element.find_element(By.XPATH, './/span[@class="rsqaWe"]')
                date_text = date_elem.text.strip()
            except:
                pass
            
            # Convert date
            exact_date = self.convert_date(date_text)
            
            # COMMENT
            comment = ""
            try:
                # Try to expand
                try:
                    more_btn = element.find_element(By.XPATH, './/button[contains(., "More") or contains(., "Plus")]')
                    self.driver.execute_script("arguments[0].click();", more_btn)
                    time.sleep(0.2)
                except:
                    pass
                
                # Get comment
                comment_elem = element.find_element(By.XPATH, './/span[@class="wiI7pd"]')
                comment = comment_elem.text.strip()
                comment = re.sub(r'\s+', ' ', comment.replace('\n', ' ').replace('\r', '')).strip()
            except:
                pass
            
            # Generate unique ID
            clean_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
            clean_date = re.sub(r'[^a-zA-Z0-9]', '_', exact_date)
            clean_location = re.sub(r'[^a-zA-Z0-9]', '_', location_name)
            unique_id = f"google_{clean_location}_{clean_name}_{clean_date}"[:100]
            
            return {
                "id": unique_id,
                "name": name,
                "source": "Google Maps",
                "location": location_name,
                "date": exact_date,
                "rating": rating,
                "comment": comment
            }
            
        except Exception as e:
            return None
    
    def convert_date(self, date_text):
        """Convert relative date to exact date (DD-MM-YYYY)"""
        if not date_text or date_text == "N/A":
            return "N/A"
        
        try:
            today = datetime.now()
            date_lower = date_text.lower()
            
            # Check for exact matches
            for pattern, days in DATE_PATTERNS.items():
                if pattern in date_lower:
                    exact_date = today - timedelta(days=days)
                    return exact_date.strftime('%d-%m-%Y')
            
            # Check for numeric patterns
            num_match = re.search(r'(\d+)\s*(?:year|years|an|ans|month|months|mois|week|weeks|semaine|semaines|day|days|jour|jours)', date_lower)
            if num_match:
                num = int(num_match.group(1))
                if 'year' in date_lower or 'an' in date_lower:
                    exact_date = today - timedelta(days=365 * num)
                elif 'month' in date_lower or 'mois' in date_lower:
                    exact_date = today - timedelta(days=30 * num)
                elif 'week' in date_lower or 'semaine' in date_lower:
                    exact_date = today - timedelta(weeks=num)
                elif 'day' in date_lower or 'jour' in date_lower:
                    exact_date = today - timedelta(days=num)
                else:
                    exact_date = today
                
                return exact_date.strftime('%d-%m-%Y')
            
            return "N/A"
            
        except:
            return "N/A"
    
    def scrape_google_location(self, url, location_name):
        """Scrape reviews from a Google Maps location"""
        try:
            # Open URL
            self.driver.get(url)
            time.sleep(3)
            
            # Handle cookies
            self.accept_cookies()
            
            # Ensure we're on reviews tab
            self.ensure_reviews_tab_open()
            
            # Scroll to load reviews
            self.scroll_to_load_reviews()
            
            # Get review elements
            review_elements = self.get_review_elements_google()
            
            if not review_elements:
                return 0, 0, 0, 0
            
            # Process reviews with progress bar
            successful = 0
            new_reviews = 0
            
            print(f"   Found {len(review_elements)} reviews. Processing...")
            with tqdm(total=len(review_elements), desc="     Parsing", leave=False, 
                     bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}') as pbar:
                for element in review_elements:
                    review_data = self.extract_google_review_data(element, location_name)
                    
                    if review_data:
                        if self.save_review(review_data):
                            new_reviews += 1
                        successful += 1
                    
                    pbar.update(1)
                    time.sleep(PROCESSING_DELAY)
            
            failed = len(review_elements) - successful
            
            return len(review_elements), successful, failed, new_reviews
            
        except Exception as e:
            print(f"   Error: {e}")
            return 0, 0, 0, 0
    
    # ========== TOP-RATED.ONLINE SCRAPING ==========
    
    def scrape_top_rated(self):
        """Scrape reviews from top-rated.online"""
        from config import OTHER_SOURCES
        source_name, url, location_name = OTHER_SOURCES[0]  # top-rated.online
        
        try:
            print(f"  Opening: {source_name}")
            self.driver.get(url)
            time.sleep(3)
            
            # Find all review blocks
            review_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.border-b")
            
            if not review_elements:
                return 0, 0, 0, 0
            
            # Process reviews
            successful = 0
            new_reviews = 0
            
            print(f"   Found {len(review_elements)} reviews. Processing...")
            with tqdm(total=len(review_elements), desc="     Parsing", leave=False, 
                     bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}') as pbar:
                
                for rev in review_elements:
                    # Extract rating
                    try:
                        rating_text = rev.find_element(By.CSS_SELECTOR, "span.text-white").text.strip()
                        rating = float(rating_text) if rating_text else 0
                    except:
                        rating = 0
                    
                    # Extract name
                    try:
                        name = rev.find_element(By.CSS_SELECTOR, "span.font-semibold a").text.strip()
                    except:
                        name = "Anonymous"
                    
                    # Extract date and source
                    date_text = "N/A"
                    try:
                        info = rev.find_element(By.CSS_SELECTOR, "div.text-sm").text.strip()
                        date_text = info.split("on Google")[0].strip()
                        # Convert date format if needed
                        exact_date = self.convert_date(date_text)
                    except:
                        exact_date = "N/A"
                    
                    # Extract comment
                    try:
                        comment = rev.find_element(By.CSS_SELECTOR, "p.text-gray-700").text.strip()
                        comment = re.sub(r'\s+', ' ', comment.replace('\n', ' ').replace('\r', '')).strip()
                    except:
                        comment = ""
                    
                    # Generate ID
                    clean_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
                    clean_date = re.sub(r'[^a-zA-Z0-9]', '_', exact_date)
                    clean_location = re.sub(r'[^a-zA-Z0-9]', '_', location_name)
                    unique_id = f"toprated_{clean_location}_{clean_name}_{clean_date}"[:100]
                    
                    # Create review data
                    review_data = {
                        "id": unique_id,
                        "name": name,
                        "source": source_name,
                        "location": location_name,
                        "date": exact_date,
                        "rating": rating,
                        "comment": comment
                    }
                    
                    # Save review
                    if self.save_review(review_data):
                        new_reviews += 1
                    successful += 1
                    
                    pbar.update(1)
                    time.sleep(PROCESSING_DELAY)
            
            failed = len(review_elements) - successful
            return len(review_elements), successful, failed, new_reviews
            
        except Exception as e:
            print(f"   Error scraping {source_name}: {e}")
            return 0, 0, 0, 0
    
    # ========== EXPAT.COM SCRAPING ==========
    
    def scrape_expat(self):
        """Scrape posts from expat.com"""
        from config import OTHER_SOURCES
        source_name, url, location_name = OTHER_SOURCES[1]  # expat.com
        
        try:
            print(f"  Opening: {source_name}")
            self.driver.get(url)
            time.sleep(5)
            
            # Find all post elements
            post_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.card-post")
            
            if not post_elements:
                return 0, 0, 0, 0
            
            # Process posts
            successful = 0
            new_reviews = 0
            
            print(f"   Found {len(post_elements)} posts. Processing...")
            with tqdm(total=len(post_elements), desc="     Parsing", leave=False, 
                     bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}') as pbar:
                
                for post in post_elements:
                    # Extract username
                    try:
                        username = post.find_element(By.CSS_SELECTOR, "a.card-post--content--author--username").text.strip()
                    except:
                        username = "Anonymous"
                    
                    # Extract date
                    try:
                        date_text = post.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime").strip()
                        # Convert to DD-MM-YYYY format
                        try:
                            dt = datetime.fromisoformat(date_text.replace('Z', '+00:00'))
                            exact_date = dt.strftime('%d-%m-%Y')
                        except:
                            exact_date = date_text
                    except:
                        exact_date = "N/A"
                    
                    # Extract message
                    try:
                        message = post.find_element(By.CSS_SELECTOR, "div.card-post--content--message").text.strip()
                        comment = re.sub(r'\s+', ' ', message.replace('\n', ' ').replace('\r', '')).strip()
                    except:
                        comment = ""
                    
                    # Generate ID
                    clean_name = re.sub(r'[^a-zA-Z0-9]', '_', username)
                    clean_date = re.sub(r'[^a-zA-Z0-9]', '_', exact_date)
                    clean_location = re.sub(r'[^a-zA-Z0-9]', '_', location_name)
                    unique_id = f"expat_{clean_location}_{clean_name}_{clean_date}"[:100]
                    
                    # Create review data (no rating for forum posts)
                    review_data = {
                        "id": unique_id,
                        "name": username,
                        "source": source_name,
                        "location": location_name,
                        "date": exact_date,
                        "rating": 0,  # Forum posts don't have ratings
                        "comment": comment
                    }
                    
                    # Save review
                    if self.save_review(review_data):
                        new_reviews += 1
                    successful += 1
                    
                    pbar.update(1)
                    time.sleep(PROCESSING_DELAY)
            
            failed = len(post_elements) - successful
            return len(post_elements), successful, failed, new_reviews
            
        except Exception as e:
            print(f"   Error scraping {source_name}: {e}")
            return 0, 0, 0, 0
    
    # ========== TRUSTBURN.COM SCRAPING ==========
    
    def scrape_trustburn(self):
        """Scrape reviews from trustburn.com"""
        from config import OTHER_SOURCES
        source_name, url, location_name = OTHER_SOURCES[2]  # trustburn.com
        
        try:
            print(f"  🌐 Opening: {source_name}")
            self.driver.get(url)
            time.sleep(5)
            
            # Find all review elements
            review_elements = self.driver.find_elements(By.CSS_SELECTOR, "article.review-card")
            
            if not review_elements:
                return 0, 0, 0, 0
            
            # Process reviews
            successful = 0
            new_reviews = 0
            
            print(f"   Found {len(review_elements)} reviews. Processing...")
            with tqdm(total=len(review_elements), desc="     Parsing", leave=False, 
                     bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}') as pbar:
                
                for review in review_elements:
                    # Extract user
                    try:
                        user = review.find_element(By.CSS_SELECTOR, "div.username span").text.strip()
                    except:
                        user = "Anonymous"
                    
                    # Extract rating
                    rating = 0
                    try:
                        stars = review.find_elements(By.CSS_SELECTOR, "i.fa-star.rate")
                        rate = 0
                        for star in stars:
                            width = star.get_attribute("style")
                            percent = int(width.replace("width:", "").replace("%;", ""))
                            rate += percent / 100
                        rating = rate 
                    except:
                        rating = 0
                    
                    # Extract date
                    try:
                        date_text = review.find_element(By.CSS_SELECTOR, "time.datetime").text.strip()
                        exact_date = self.convert_date(date_text)
                    except:
                        exact_date = "N/A"
                    
                    # Extract comment
                    try:
                        msg = review.find_element(By.CSS_SELECTOR, "p.text").text.strip()
                        comment = re.sub(r'\s+', ' ', msg.replace('\n', ' ').replace('\r', '')).strip()
                    except:
                        comment = ""
                    
                    # Generate ID
                    clean_name = re.sub(r'[^a-zA-Z0-9]', '_', user)
                    clean_date = re.sub(r'[^a-zA-Z0-9]', '_', exact_date)
                    clean_location = re.sub(r'[^a-zA-Z0-9]', '_', location_name)
                    unique_id = f"trustburn_{clean_location}_{clean_name}_{clean_date}"[:100]
                    
                    # Create review data
                    review_data = {
                        "id": unique_id,
                        "name": user,
                        "source": source_name,
                        "location": location_name,
                        "date": exact_date,
                        "rating": rating,
                        "comment": comment
                    }
                    
                    # Save review
                    if self.save_review(review_data):
                        new_reviews += 1
                    successful += 1
                    
                    pbar.update(1)
                    time.sleep(PROCESSING_DELAY)
            
            failed = len(review_elements) - successful
            return len(review_elements), successful, failed, new_reviews
            
        except Exception as e:
            print(f"   Error scraping {source_name}: {e}")
            return 0, 0, 0, 0
    
    def get_total_reviews(self):
        """Get total number of reviews in CSV"""
        try:
            if os.path.exists(self.csv_filename):
                with open(self.csv_filename, 'r', encoding=CSV_ENCODING) as f:
                    return sum(1 for line in f) - 1
            return 0
        except:
            return 0
    
    def close(self):
        """Close the browser"""
        if hasattr(self, 'driver'):
            self.driver.quit()