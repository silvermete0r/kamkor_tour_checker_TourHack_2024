from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

def parse_website():
    try:
        url = "https://www.fondkamkor.kz/ru/Voucher/partner/packets/tour/search_operator"
        
        # Setting up the Selenium WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        
        # Waiting for the content to load
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "tsCompany")))
        
        # Extracting the HTML content after the content is loaded
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Finding the tour operator table
        tour_operators = soup.findAll('div', class_='tsCompany')

        tour_operators_data = []

        # Looping through each tour operator
        for tour_operator in tour_operators:
            number = tour_operator.find('div', class_='tsCompanyNumber').text
            name = tour_operator.find('div', class_='tsCompanyName').text
            contacts = tour_operator.find('div', class_='tsCompanyContacts')
            address = contacts.findAll('span', class_='tsValue')[0].text if len(contacts.findAll('span', class_='tsValue')) > 0 else None
            phone = contacts.findAll('span', class_='tsValue')[1].text if len(contacts.findAll('span', class_='tsValue')) > 1 else None
            website = contacts.find('a').get('href') if contacts.find('a') else None
            requisites = tour_operator.find('div', class_='tsCompanyRequisites')
            license = requisites.findAll('span', class_='tsValue')[0].text if len(requisites.findAll('span', class_='tsValue')) > 0 else None
            bank_guarantee = requisites.findAll('span', class_='tsValue')[1].text if len(requisites.findAll('span', class_='tsValue')) > 1 else None
            
            tour_operator_info = {
                'number': number,
                'name': name,
                'address': address,
                'phone': phone,
                'website': website,
                'license': license,
                'bank_guarantee': bank_guarantee
            }

            tour_operators_data.append(tour_operator_info)
            print(tour_operator_info)

        return tour_operators_data

    except Exception as e:
        print(e)
    finally:
        # Closing the WebDriver
        driver.quit()

tour_operators_data = parse_website()

with open('data/tour_operators_data.json', 'w', encoding="utf-8") as file:
    json.dump(tour_operators_data, file, ensure_ascii=False, indent=4)