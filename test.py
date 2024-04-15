from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

class IMDbScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.meta_tags = []
        self.seo_tags = []
        self.title_tag = None

    def get_web_info(self) -> None:
        url = 'https://www.imdb.com/chart/top'
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ipc-metadata-list')))

        self.meta_tags = self.driver.find_elements(By.TAG_NAME, 'meta')
        self.seo_tags = self.driver.find_elements(By.XPATH, '//link[@rel="canonical"]')
        self.title_tag = self.driver.find_element(By.TAG_NAME, 'title')

    def create_text_file(self) -> None:
        output_file = 'web_info.txt'
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("Meta Tags:\n")
            for meta_tag in self.meta_tags:
                name = meta_tag.get_attribute('name')
                property = meta_tag.get_attribute('property')
                content = meta_tag.get_attribute('content')
                if name:
                    file.write(f"Name: {name}, Content: {content}\n")
                elif property:
                    file.write(f"Property: {property}, Content: {content}\n")
                else:
                    file.write(f"Content: {content}\n")

            file.write("\nSEO Tags:\n")
            for seo_tag in self.seo_tags:
                file.write(seo_tag.get_attribute('href') + '\n')

            file.write("\nTitle:\n")
            file.write(self.title_tag.get_attribute('innerText') + '\n')
        print(f"ข้อมูลถูกบันทึกลงในไฟล์ {output_file} แล้ว")

    def scrape_imdb_top_movies(self) -> None:
        ul_element = self.driver.find_element(By.CLASS_NAME, 'ipc-metadata-list')
        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

        data = []

        for li in li_elements:
            title_element = li.find_element(By.CLASS_NAME, 'ipc-title__text')
            rate_element = li.find_element(By.CLASS_NAME, 'ipc-rating-star')
            title_metadata_div = li.find_element(By.CLASS_NAME, 'cli-title-metadata')
            spans = title_metadata_div.find_elements(By.TAG_NAME, 'span')
            second_span_text = ""
            if len(spans) >= 2:
                first_span_text = spans[0].text
                second_span_text = spans[1].text
            title = title_element.text
            title_name  = title.split('.')[1].strip()

            rate = rate_element.get_attribute('textContent')
            data.append({'Title': title_name, 'Rate': rate, 'Year': first_span_text, 'Length': second_span_text})

        df = pd.DataFrame(data)
        df.index = df.index + 1
        df.to_csv('imdb_top_movies.csv', index=True)
        print("ข้อมูลถูกบันทึกลงในไฟล์ imdb_top_movies.csv แล้ว")

    def close_driver(self) -> None:
        self.driver.quit()

# ใช้งานคลาส IMDbScraper
scraper = IMDbScraper()
scraper.get_web_info()
scraper.create_text_file()
scraper.scrape_imdb_top_movies()
scraper.close_driver()
