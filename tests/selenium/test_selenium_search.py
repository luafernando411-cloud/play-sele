import os
from urllib.parse import urlencode

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_search_with_selenium() -> None:
    query = "Python automation testing"
    url = f"https://en.wikipedia.org/w/index.php?{urlencode({'search': query})}"
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if chrome_bin := os.environ.get("CHROME_BIN"):
        options.binary_location = chrome_bin

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".mw-search-result-heading a")
            )
        )
        assert result.text.strip(), "O primeiro resultado da busca veio sem título."
        print(f"Resultado Selenium: {result.text}")
    finally:
        driver.quit()


if __name__ == "__main__":
    test_search_with_selenium()
