from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set the phone number to search
phone_number = "+917500706369"

# Define search queries for social media
search_urls = [
    f"https://www.google.com/search?q={phone_number}+site:facebook.com",
    f"https://www.google.com/search?q={phone_number}+site:instagram.com",
    f"https://www.google.com/search?q={phone_number}+site:twitter.com",
    f"https://www.google.com/search?q={phone_number}+site:linkedin.com",
]

# Set up the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Runs in the background (no browser window)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Perform searches
for url in search_urls:
    print(f"\n🔍 Searching: {url}")
    driver.get(url)
    time.sleep(3)  # Wait for page to load
    
    # Extract search results
    results = driver.find_elements(By.CSS_SELECTOR, "h3")
    
    if results:
        print("✅ Possible Accounts Found:")
        for result in results[:5]:  # Show top 5 results
            print("- " + result.text)
    else:
        print("❌ No results found.")

# Close the driver
driver.quit()
