import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv


url_list = ["https://www.spr.kz/astana/turagentstva/", 
            'https://www.spr.kz/almati/turagentstva/',
            'https://www.spr.kz/shimkent/turagentstva/']

with open('tour_agents.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Good', 'Bad'])  # Write header


def extract(search_url):
    # Setting up the Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(search_url)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "rubricContainer")))

    # Extracting the HTML content after the content is loaded
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # extract the link of first company in the list
    search_result = soup.find('div', class_='rubricContainer')
    with open('tour_agents.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for i in search_result.find_all('div', class_='item'):
            name = i.find('b').text
            good = i.find('span', class_='good').text
            bad = i.find('span', class_='bad').text
            writer.writerow([name, good, bad])

for i in url_list:
     extract(i)