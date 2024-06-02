from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
import time
import datetime
import numpy as np
import pandas as pd
import random

def get_hotels_list(driver):
    print("Starting to scrape hotels list data")
    page_source = driver.page_source
    doc = BeautifulSoup(page_source, 'html.parser')
    hotels_list = doc.find_all('div', class_='uitk-card uitk-card-roundcorner-all uitk-card-has-border uitk-card-has-primary-theme')
    print(f"Extract hotels list worked successfully")
    return hotels_list

def get_data_from_dates(start_date, end_date, temp_df, hotels_df, driver):
    print(f"Starting to scrape data from dates: {start_date}-{end_date}")
    url = f"https://expedia.com/Hotel-Search?adults=2&d1={start_date}&d2={end_date}&destination=New%20York%20%28and%20vicinity%29%2C%20New%20York%2C%20United%20States%20of%20America&endDate={end_date}&latLong=40.75668%2C-73.98647&regionId=178293&rooms=1&semdtl=&sort=RECOMMENDED&startDate={start_date}&theme=&useRewards=false&userIntent="
    open_url(driver, url)
    hotels_list = get_hotels_list(driver)
    temp_df = hotels_to_df(hotels_list, temp_df, start_date, end_date)
    hotels_df = pd.concat([hotels_df, temp_df], ignore_index=True, axis=0)
    print(f"Data extracted successfully: {hotels_df}")
    return hotels_df

def hotels_to_df(hotels_list, df, start_date, end_date):
    print("Starting to extract data from hotels list into df")
    for i, hotel in enumerate(hotels_list):
        try:
            df.at[i, 'Snapshot'] = pd.Timestamp.today()
            df.at[i, 'Index'] = i
            df.at[i, 'Hotel Name'] = hotel.find('h3').text
            df.at[i, 'TTT'] = (start_date - datetime.date.today()).days
            df.at[i, 'LOS'] = (end_date - start_date).days
            grade_element = hotel.find('span', class_='uitk-badge uitk-badge-base-large uitk-badge-base-has-text uitk-badge-positive')
            df.at[i, 'Grade'] = grade_element.text if grade_element is not None else np.nan
            reviews_element = hotel.find_all('span', class_="uitk-text uitk-type-200 uitk-type-regular uitk-text-default-theme")
            df.at[i, 'Num of Reviews'] = reviews_element[-1].text if len(reviews_element) > 0 else np.nan
            prices_list = hotel.find_all('div', class_="uitk-text uitk-type-300 uitk-text-default-theme is-visually-hidden")
            if len(prices_list) > 1:
                df.at[i, 'Curr Price'] = prices_list[1].text
                df.at[i, 'Original Price'] = prices_list[0].text
            else:
                df.at[i, 'Curr Price'] = prices_list[0].text
                df.at[i, 'Original Price'] = np.nan
            df.at[i, 'Percentage of discount'] = 0  # Placeholder, needs calculation logic if required
            df.at[i, 'Distance from center'] = 0  # Placeholder, needs extraction logic if available
            df.at[i, 'Type of room'] = 0  # Placeholder, needs extraction logic if available
            df.at[i, 'Location grade'] = 0  # Placeholder, needs extraction logic if available
            refundable_element = hotel.find('div', class_="uitk-text uitk-type-300 uitk-text-positive-theme")
            if refundable_element and 'refundable' in refundable_element.text.lower():
                df.at[i, 'Is refundable'] = True
            else:
                df.at[i, 'Is refundable'] = False
            late_payment_element = hotel.find('div', class_="uitk-text uitk-type-300 uitk-text-positive-theme")
            if late_payment_element and 'later' in late_payment_element.text.lower():
                df.at[i, 'Late payment'] = True
            else:
                df.at[i, 'Late payment'] = False
            included_element = hotel.find('div', class_="uitk-text truncate-lines-2 uitk-type-200 uitk-text-default-theme")
            df.at[i, 'Breakfast included'] = included_element.text if included_element else np.nan
            member_btn = hotel.find('a', class_='uitk-button uitk-button-small uitk-button-has-text uitk-button-as-link uitk-button-primary uitk-layout-flex-item-align-self-flex-end uitk-layout-flex-item')
            df.at[i, 'Option Member'] = True if member_btn else False
        except Exception as e:
            print(f'Error at hotel element: {i} | {e}')
            continue

    print(f"Successfully finished creating df:\n{df}")
    return df

def open_url(driver, url):
    driver.get(url)
    ScrollNumber = 4
    for _ in range(ScrollNumber):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            show_more_btn = driver.find_element("css selector", 'button[class="uitk-button uitk-button-medium uitk-button-has-text uitk-button-secondary"]')
            if show_more_btn:
                driver.execute_script("arguments[0].click();", show_more_btn)
        except Exception as e:
            print(f"Failed while trying to click on show more button | {e}")
        time.sleep(5)

def main():
    # Creates a Chrome driver to start scraping data via browser
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36")
    options.add_argument("disable-infobars")
    options.add_argument('accept-encoding=gzip, deflate, br')
    options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
    options.add_argument('referer=https://www.expedia.com/')
    options.add_argument('upgrade-insecure-requests=1')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Create a dataframe - should handle all the data from the expedia site for each hotel that exist
    hotels_df = pd.DataFrame(columns=['Snapshot',
                                      'Index',
                                      'Hotel Name',
                                      'TTT',
                                      'LOS',
                                      'Grade',
                                      'Num of Reviews',
                                      'Curr Price',
                                      'Original Price',
                                      'Percentage of discount',
                                      'Distance from center',
                                      'Type of room',
                                      'Location grade',
                                      'Is refundable',
                                      'Late payment',
                                      'Breakfast included',
                                      'Option Member'])

    temp_df = hotels_df.copy()

    for i in range(1, 31):
        for j in range(1, 6):
            try:
                start_date = datetime.date.today() + datetime.timedelta(days=i)
                end_date = start_date + datetime.timedelta(days=j)
                hotels_df = get_data_from_dates(start_date, end_date, temp_df, hotels_df, driver)
                temp_df.drop(temp_df.index, inplace=True)
            except Exception as e:
                print(f"Error at dates: {start_date} - {end_date} | {e}")

    last_output_df = hotels_df.copy()
    last_output_df.to_csv(r"C:\Users\User\Desktop\last_output_df.csv", index=False)

if __name__ == '__main__':
    main()
