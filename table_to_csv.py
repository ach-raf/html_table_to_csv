# Importing the required modules
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

PATH_TO_CHROME_DRIVER = r'C:\PATH\TO\chromedriver.exe'


def table_find_by_id(_soup, _table_id):
    return _soup.find('table', id=_table_id)


def table_find_by_class(_soup, _class):
    return _soup.find('table', {'class': _class})


def table_to_csv(_table, _csv_save_path):
    _header = _table.find('tr')
    data = []
    list_header = []
    for items in _header:
        try:
            list_header.append(items.get_text())
        except:
            continue

    # for getting the data
    HTML_data = _table.find_all('tr')[1:]
    for element in HTML_data:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text().strip())
            except:
                continue
        data.append(sub_data)

    # Storing the data into Pandas
    # DataFrame
    dataFrame = pd.DataFrame(data=data, columns=list_header)

    # Converting Pandas DataFrame
    # into CSV file
    dataFrame.to_csv(_csv_save_path)


def main(_link, _table_id, _csv_save_path):
    options = Options()
    options.add_argument("--headless")
    options.headless = True

    browser = webdriver.Chrome(executable_path=PATH_TO_CHROME_DRIVER, options=options)
    # browser.implicitly_wait(20)
    browser.get(_link)
    browser.minimize_window()
    time.sleep(2)
    _html = browser.page_source
    soup = BeautifulSoup(_html, 'lxml')
    # find table by id
    table = table_find_by_id(soup, _table_id)

    # find table by class
    # table = table_find_by_class(soup, _table_id)

    table_to_csv(table, _csv_save_path)
    browser.quit()


link = 'https://ark-funds.com/arkk'
table_id = 'top10h'
csv_save_path = 'arkk.csv'
main(link, table_id, csv_save_path)
