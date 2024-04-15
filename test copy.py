from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

# สร้าง WebDriver เป็นตัวแปร global
driver = webdriver.Chrome()
url = 'https://www.imdb.com/chart/top'
driver.get(url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ipc-metadata-list')))

def get_web_info()-> tuple[List[WebElement], List[WebElement], WebElement]:
    # ดึงข้อมูล meta, SEO, และ title ของหน้าเว็บ
    meta_tags = driver.find_elements(By.TAG_NAME, 'meta')
    seo_tags = driver.find_elements(By.XPATH, '//link[@rel="canonical"]')
    title_tag = driver.find_element(By.TAG_NAME, 'title')

    # แสดงผลข้อมูล
    print("Meta Tags:")
    for meta_tag in meta_tags:
        name = meta_tag.get_attribute('name')
        property = meta_tag.get_attribute('property')
        content = meta_tag.get_attribute('content')
        if name:
            print(f"Name: {name}, Content: {content}")
        elif property:
            print(f"Property: {property}, Content: {content}")
        else:
            print(f"Content: {content}")

    print("\nSEO Tags:")
    for seo_tag in seo_tags:
        print(seo_tag.get_attribute('href'))

    print("\nTitle:")
    print(title_tag.get_attribute('innerText'))

    return meta_tags, seo_tags, title_tag

def create_text_file(meta_tags: List[WebElement], seo_tags: List[WebElement], title_tag: WebElement)-> None:
    output_file = 'web_info.txt'
    # เปิดไฟล์เพื่อเขียนข้อมูล
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("Meta Tags:\n")
        for meta_tag in meta_tags:
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
        for seo_tag in seo_tags:
            file.write(seo_tag.get_attribute('href') + '\n')

        file.write("\nTitle:\n")
        file.write(title_tag.get_attribute('innerText') + '\n')
    print(f"ข้อมูลถูกบันทึกลงในไฟล์ {output_file} แล้ว")

def scrape_imdb_top_movies():
    ul_element = driver.find_element(By.CLASS_NAME, 'ipc-metadata-list')
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

# ทำงานด้วยฟังก์ชันที่กำหนดขึ้น
meta_tags, seo_tags, title_tag = get_web_info()
create_text_file(meta_tags, seo_tags, title_tag)
scrape_imdb_top_movies()

# ปิด WebDriver ภายในตัวสุดท้ายของโปรแกรม
driver.quit()
