import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize WebDriver using webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL to scrape
url = 'https://news.metal.com/list/industry/aluminium'
driver.get(url)

# Wait for the page to load
wait = WebDriverWait(driver, 10)

# Scroll and load more news
while True:
    try:
        more_news_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.footer___PvIjk span')))
        
        # Use ActionChains to move to the element and click
        actions = ActionChains(driver)
        actions.move_to_element(more_news_button).click().perform()
        
        time.sleep(2)  # wait for new articles to load
    except Exception as e:
        print("No more 'more news' button found or error occurred:", e)
        break

# Fetch the page source after all articles are loaded
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the WebDriver
driver.quit()

# Extract news articles details
articles = []
for item in soup.select('div.newsItem___wZtKx'):
    try:
        title = item.select_one('div.newsItemContent___2oFIU a').text.strip()
        summary = item.select_one('div.description___z7ktb').text.strip()
        date_str = item.select_one('div.date___3dzkE').text.strip()
        date = datetime.strptime(date_str, '%b %d, %Y %H:%M')
        
        # Print the date and title for debugging
        print(f"Date: {date}, Title: {title}")
        
        # Filter articles within the last 45 days
        if date >= datetime.now() - timedelta(days=45):
            articles.append({'title': title, 'summary': summary, 'date': date})
    except Exception as e:
        print(f"Error processing item: {e}")

# Convert to DataFrame
df = pd.DataFrame(articles)

# Save DataFrame to CSV
df.to_csv('Extracted data.csv', index=False, date_format='%Y-%m-%d %H:%M:%S')
