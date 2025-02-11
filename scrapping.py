from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=service, options=options)

# Ganti dengan URL halaman review toko di Tokopedia
url = "https://www.tokopedia.com/dkmall/review"

driver.get(url)

reviews = []

while True:
    # Ambil elemen review
    time.sleep(3)  # Tunggu halaman masuk
    soup = BeautifulSoup(driver.page_source, "html.parser")
    try:
        review_elements = soup.findAll("article", attrs={'class':'css-ccpe8t'})

        for review in review_elements:
            username = review.find("span", attrs={"class":"name"}).text
            comment = review.find("span", attrs={"data-testid":"lblItemUlasan"}).text
            product_container = review.findAll("a",attrs={"class":"styProduct"})

            for element in product_container:
                product = review.find("p", attrs={"data-unify":"Typography"}).text
                
                reviews.append({
                    "username": username,
                    "review": comment,
                    "product": product
                })
    except:
        print("there is error")
        
    # Cek apakah ada tombol "Next" untuk lanjut ke halaman berikutnya
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Laman berikutnya"]')
        next_button.click()
        time.sleep(2)
    except:
        print("No more pages.")
        break  # Keluar jika tidak ada tombol "Next"

driver.quit()

# Simpan ke CSV
df = pd.DataFrame(reviews)
df.to_csv("tokopedia_reviews.csv", index=False)
print("Scraping selesai! Data disimpan dalam tokopedia_reviews.csv")
