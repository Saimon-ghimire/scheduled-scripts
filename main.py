from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import pandas as pd
import os

file=open('temp','a')
file.write('apple')
file.close()
# For cron job
os.environ["PATH"] += ":/usr/local/bin/"

options = Options()
options.add_argument("--headless")
driver = None
try:
    driver = webdriver.Firefox(options=options)
    driver.get("https://kalimatimarket.gov.np/lang/en")
    driver.get("https://kalimatimarket.gov.np/price")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "odd"))
    )

    odd_rows = driver.find_elements(By.CLASS_NAME, "odd")
    even_rows = driver.find_elements(By.CLASS_NAME, "even")

    today = date.today()
    filename = os.path.join(os.path.dirname(__file__), f"{today}.csv")
    header = ["Name", "Unit", "Minimum", "Maximum", "Average"]

    def write_to_file(row):
        data_elements = [item.text for item in row.find_elements(By.TAG_NAME, "td")]
        pd.DataFrame([data_elements]).to_csv(
            filename, mode="a", index=False, header=False
        )

    # opened the file in write mode to ensure a clean empty file
    with open(filename, "w") as file:
        pd.DataFrame([header]).to_csv(file, index=False, header=False)

    # Combine odd and even rows into one list and process
    for row in odd_rows + even_rows:
        write_to_file(row)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if driver:
        driver.quit()
