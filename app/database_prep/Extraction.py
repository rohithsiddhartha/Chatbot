import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException


# Global variable to store the ChromeDriver path
CHROME_DRIVER_PATH = None

def get_chrome_driver_path():
    global CHROME_DRIVER_PATH
    if CHROME_DRIVER_PATH is None:
        CHROME_DRIVER_PATH = ChromeDriverManager().install()
    return CHROME_DRIVER_PATH

def extract_text_with_selenium(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        # Use the cached ChromeDriver path
        service = Service(get_chrome_driver_path())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Navigate to the URL
        driver.get(url)

        # Wait for the page to load (adjust the timeout as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Extract text from the page
        body_element = driver.find_element(By.TAG_NAME, "body")
        text_content = body_element.text

        return text_content

    except TimeoutException:
        print(f"Timeout occurred while loading the page: {url}")
        return None
    except WebDriverException as e:
        print(f"WebDriver exception occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    finally:
        if driver:
            driver.quit()

import os

def save_text_to_file(text, url, folder_name="text"):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Create a valid file name based on the URL
    file_name = url.replace("https://", "").replace("/", "_") + ".txt"
    file_path = os.path.join(folder_name, file_name)
    
    # Save the text to a file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)
    
    print(f"Text saved to {file_path}")


if __name__ == "__main__":
    list_of_urls = [
        "https://www.artisan.co/ai-sales-agent",
        "https://artisan.co",
        "https://hiretop.com/blog2/artisan-ava-ai-employee/",
        "https://support.artisan.co/en/articles/9253672-getting-started-with-artisan-sales",
        "https://www.artisan.co/products/sales-automation",
        "https://support.artisan.co/en/articles/9191300-what-is-email-warmup",
        "https://support.artisan.co/en/articles/9191306-help-ava-is-sending-strange-messages-from-my-email",
        "https://support.artisan.co/en/articles/9191308-how-do-i-upload-a-csv-file-of-my-own-leads",
        "https://support.artisan.co/en/articles/9191337-ava-isn-t-sending-out-my-emails-why",
        "https://support.artisan.co/en/articles/9226514-how-to-create-a-new-campaign"
    ]

    for url in list_of_urls:
        extracted_text = extract_text_with_selenium(url)
        if extracted_text:
            print(extracted_text)
            print("*" * 100)
            save_text_to_file(extracted_text, url, "text2")
        else:
            print(f"Failed to extract text from URL: {url}")
