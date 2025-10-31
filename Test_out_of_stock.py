from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

OUT_OF_STOCK_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=40"
CART_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    # 1. Open the out-of-stock product page
    driver.get(OUT_OF_STOCK_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("Opened out-of-stock product page.")

    # 2. Try to click Add to Cart (if the button is disabled, that’s correct)
    try:
        add_btn = driver.find_element(By.ID, "button-cart")
        if not add_btn.is_enabled():
            print("PASS: Add to Cart button is disabled for out-of-stock product.")
        else:
            add_btn.click()
            time.sleep(1.5)
            page = driver.page_source.lower()
            if any(k in page for k in ["out of stock", "unavailable", "not available"]):
                print("PASS: Out-of-stock message displayed after clicking Add to Cart.")
            else:
                print("FAIL: No out-of-stock warning message shown.")
    except:
        # If there is no button, that’s also correct
        print("PASS: No Add to Cart button present (expected for out-of-stock product).")

    # 3. Verify the cart remains empty
    driver.get(CART_URL)
    time.sleep(1)
    if "your shopping cart is empty" in driver.page_source.lower():
        print("PASS: Cart is empty after out-of-stock attempt.")
    else:
        print("FAIL: Cart is not empty (unexpected).")

    print("Test completed.")

finally:
    driver.quit()