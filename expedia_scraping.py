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
    print("starting to scrape hotels list data")
    page_source = driver.page_source
    doc = BeautifulSoup(page_source, 'html.parser')
    hotels_list = doc.find_all('div', class_='uitk-card uitk-card-roundcorner-all uitk-card-has-border uitk-card-has-primary-theme')
    print(f"extract hotels list succeed: {hotels_list}")
    return hotels_list


def get_data_from_dates(start_date, end_date, temp_df, hotels_df, driver):
    print(f"starting to scrape data from dates: {start_date}-{end_date}")
    url = "https://expedia.com/Hotel-Search?adults=2&d1={start_date}&d2={end_date}&destination=New%20York%20%28and%20vicinity%29%2C%20New%20York%2C%20United%20States%20of%20America&endDate={end_date}&latLong=40.75668%2C-73.98647&regionId=178293&rooms=1&semdtl=&sort=RECOMMENDED&startDate={start_date}&theme=&useRewards=false&userIntent=".format(start_date=start_date, end_date=end_date)
    open_url(driver, url)
    hotels_list = get_hotels_list(driver)
    temp_df = hotels_to_df(hotels_list,temp_df,start_date, end_date)
    contact_df = pd.concat([hotels_df, temp_df], ignore_index=True, axis=0)
    print(f"concat df: {contact_df}")
    return contact_df


def hotels_to_df(hotels_list, df, start_date,
                 end_date):  # Function receives list of hotels, dataframe to insert the data into, start and end date
    print("starting to convert hotels list data into df")
    for i in range(0, 180):
        try:
            df.at[i, 'Snapshot'] = pd.Timestamp.today()
            df.loc[i, 'Index'] = i
            df.at[i, 'Hotel Name'] = hotels_list[i].find('h3').text
            df.at[i, 'TTT'] = (start_date - datetime.date.today()).days
            df.at[i, 'LOS'] = (end_date - start_date).days
            grade_element = hotels_list[i].find('span',
                                                class_='uitk-badge uitk-badge-base-large uitk-badge-base-has-text uitk-badge-positive')
            df.at[i, 'Grade'] = grade_element.text if grade_element is not None else np.nan
            reviews_element = hotels_list[i].find_all('span', class_="uitk-text uitk-type-200 uitk-type-regular uitk-text-default-theme")
            df.at[i, 'Num of Reviews'] = reviews_element[-1].text if len(reviews_element) > 0 else np.nan
            prices_list = hotels_list[i].find_all('div',
                                                  class_="uitk-text uitk-type-300 uitk-text-default-theme is-visually-hidden")
            df.at[i, 'Curr Price'] = prices_list[1].text if len(prices_list) > 1 else prices_list[0].text
            df.at[i, 'Original Price'] = prices_list[0].text if len(prices_list) > 1 else np.nan
            df.at[i, 'Percentage of discount'] = 0
            df.at[i, 'Distance from center'] = 0
            df.at[i, 'Type of room'] = 0
            df.at[i, 'Location grade'] = 0
            refundable_element = hotels_list[i].find('div',
                                                     class_="uitk-layout-flex uitk-layout-flex-flex-direction-column uitk-layout-flex-gap-three").find_all(
                'span')
            df.at[i, 'Is refundable'] = True if len(refundable_element) > 0 and refundable_element[0].text.__contains__(
                'refundable') else False
            late_payment_element = hotels_list[i].find('div',
                                                       class_="uitk-layout-flex uitk-layout-flex-flex-direction-column uitk-layout-flex-gap-three").find_all(
                'span')
            df.at[i, 'Late payment'] = True if len(late_payment_element) > 0 and late_payment_element[
                -1].text.__contains__('later') else False
            included_element = hotels_list[i].find('div',
                                                   class_="uitk-text truncate uitk-type-200 uitk-text-default-theme")
            df.at[i, 'Breakfast included'] = included_element.text if included_element is not None else np.nan
            member_btn = hotels_list[i].find('a',
                                             class_='uitk-button uitk-button-small uitk-button-has-text uitk-button-as-link uitk-button-primary uitk-layout-flex-item-align-self-flex-end uitk-layout-flex-item')
            df.at[i, 'Option Member'] = True if member_btn else False
        except Exception as e:
            print(f'error at hotel number: {i} | {e}')

    print(f"Successfuly finished to create df:\n{df[["Grade", "Num of Reviews"]]}")
    return df


def open_url(driver, url):
    driver.get(url)
    ScrollNumber = 4
    for i in range(1,ScrollNumber):
        driver.execute_script("window.scrollTo(1,5000000)")
        show_more_btn = driver.find_element("xpath", '//*[@id="app-layer-base"]/div/main/div/div/div/div/div[2]/section[2]/div/div[2]/div/div[2]/div[1]/div[4]/section/button')
        if show_more_btn:
            driver.execute_script("arguments[0].click();", show_more_btn)
        else: print("Button not found")
        time.sleep(5)


def main():
    # Creates a Chrome driver to start scraping data via browser
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36")
    options.add_argument("disable-infobars")
    options.add_argument('accept-encoding=gzip, deflate, br')
    options.add_argument(
        'accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
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
    # open_url(driver, test_url)

    for i in range(1, 31):
        for j in range(1, 6):
            try:
                start_date = datetime.date.today() + datetime.timedelta(days=i)
                end_date = start_date + datetime.timedelta(days=j)
                hotels_df = get_data_from_dates(start_date, end_date, temp_df, hotels_df, driver)
                temp_df.drop(temp_df.index, inplace=True)
            except Exception as e:
                print(f"error at dates: {start_date} - {end_date} | {e}")

    last_output_df = hotels_df.copy()
    last_output_df.to_csv(r"C:\Users\User\Desktop\last_output_df.csv", index=False)


if __name__ == '__main__':
    test_url = "https://www.expedia.com/Hotel-Search?destination=New+York+%28and+vicinity%29%2C+New+York%2C+United+States+of+America&regionId=178293&latLong=40.75668%2C-73.98647&flexibility=0_DAY&d1=2024-05-26&startDate=2024-05-26&d2=2024-05-27&endDate=2024-05-27&adults=2&rooms=1&theme=&userIntent=&semdtl=&useRewards=false&sort=RECOMMENDED"
    main()