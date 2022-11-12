import time

import undetected_chromedriver
import pandas as pd

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os_dict = {}


def create_pandas_series():
    os_series = pd.Series(os_dict)
    print(os_series.sort_values(ascending=False))


def start_webdriver():
    options = undetected_chromedriver.ChromeOptions()
    driver = undetected_chromedriver.Chrome(options=options)

    return driver


def get_smartphone(url):
    driver = start_webdriver()
    wait = WebDriverWait(driver, 10)
    driver.get(url)

    try:
        wait.until(EC.element_to_be_clickable((By.ID, 'section-characteristics')))
        try:
            test_xpath = driver.find_element(By.XPATH, '//span[contains(text(), "Версия")]/ancestor::dl/dd')
            os_version = test_xpath.text.split('.')[0]
            if os_version not in os_dict:
                os_dict[os_version] = 0
            os_dict[os_version] += 1
        except NoSuchElementException:
            print(f'Не удалось спарсить {url}')

    except TimeoutException:
        print('Страница не прогрузилась')

    driver.close()
    driver.quit()


def init_selenium(url):
    driver = start_webdriver()
    driver.get(url)
    while sum(os_dict.values()) < 100:

        time.sleep(3)
        links = driver.find_elements(By.XPATH, '//a[contains(@class, "k8n")]')

        for element in links:
            if sum(os_dict.values()) < 100:
                get_smartphone(element.get_attribute('href'))

        next_page = driver.find_element(By.XPATH, '//div[@class="al9a _4-a"]')
        next_page.click()

    driver.close()
    driver.quit()

    create_pandas_series()


if __name__ == '__main__':
    url = 'https://www.ozon.ru/category/smartfony-15502/?sorting=rating'
    init_selenium(url)
