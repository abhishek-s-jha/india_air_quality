import os
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

df_1 = pd.read_csv('./processed_station_geo_loc.csv')
df_2 = pd.read_csv('./stations_region.csv')
df = pd.merge(df_1, df_2, on='name')
df.head()

df.sort_values(['state', 'city'], inplace=True)
df.reset_index(drop=True, inplace=True)

def fill_data(field_name, value):
    
    if field_name == 'state':
        field_box_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-availability/div/div/div/div/div/div/div[1]/div[1]/div/ng-select/div/div/div[1]'
        field_box_text = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-availability/div/div/div/div/div/div/div[1]/div[1]/div/ng-select/select-dropdown/div/div[1]/input'
        text = value
        
    elif field_name == 'city':
        field_box_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-availability/div/div/div/div/div/div/div[1]/div[2]/div/ng-select/div/div/div[1]'
        field_box_text = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-availability/div/div/div/div/div/div/div[1]/div[2]/div/ng-select/select-dropdown/div/div[1]/input'
        text = value
        
    elif field_name == 'station':
        field_box_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-availability/div/div/div/div/div/div/div[1]/div[3]/div/ng-select/div/div/div[1]'
        field_box_text = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-availability/div/div/div/div/div/div/div[1]/div[3]/div/ng-select/select-dropdown/div/div[1]/input'
        text = value
        
    if value=='Noida':
        field_box_click_action = driver.find_element_by_xpath(field_box_click)
        field_box_click_action.click()
        
        field_box_text_action = driver.find_element_by_xpath(field_box_text)
        field_box_text_action.send_keys(text)

        city_click = driver.find_element_by_xpath('/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-availability/div/div/div/div/div/div/div[1]/div[2]/div/ng-select/select-dropdown/div/div[2]/ul/li[2]')
        city_click.click()
        
    else:
        field_box_click_action = driver.find_element_by_xpath(field_box_click)
        field_box_click_action.click()

        field_box_text_action = driver.find_element_by_xpath(field_box_text)
        field_box_text_action.send_keys(text)

        field_box_text_action.send_keys(Keys.ENTER)
    

driver = webdriver.Chrome('/usr/bin/chromedriver')
sleep(10)
driver.get('https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing')
sleep(50)
driver.get('https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing/caaqm-data-availability')
sleep(15)

root_dir = "./stations_start_info"
if not os.path.exists(root_dir):
    os.mkdir(root_dir)
    
dummy_df = pd.read_csv(os.path.join(root_dir,"dummy.csv"))

error_idx = []
for idx in range(len(df)):
    
    if idx > 430:
    
        state = df.state[idx]
        city = df.city[idx]
        station_id = df.id[idx]
        station_name = df.name[idx]

        print(f"{idx}. {state} :: {city} :: {station_id} :: {station_name} :: ", end='')

        file_path = os.path.join(root_dir, state)
        if not os.path.exists(file_path):
            os.mkdir(file_path)

        try:
            # Find the button using XPath and click it
            # Clearing previous details filled in each field
            button = driver.find_element_by_xpath('/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-availability/div/div/div/div/div/div/div[1]/div[1]/div/ng-select/div/div/div[2]')
            button.click()

            sleep(1)

            fill_data(field_name='state', value=state)
            sleep(1)
            fill_data(field_name='city', value=city)
            sleep(1)
            fill_data(field_name='station', value=station_name)
            sleep(1)

            # Find the button using XPath and click it
            button = driver.find_element_by_xpath('/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-availability/div/div/div/div/div/div/div[1]/div[4]/div/button')
            button.click()

            sleep(35)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find('table', {'class': 'table-hover'})

            headers = []
            rows = []
            for tr in table.tbody.find_all('tr'):
                row = []
                for td in tr.find_all('td'):
                    row.append(td.text.strip())
                rows.append(row)

            for th in table.thead.find_all('th'):
                headers.append(th.text.strip())

            df_1 = pd.DataFrame(rows, columns=headers)

            if df_1.equals(dummy_df):
                print("ERROR", end='\n\n')
                error_idx.append(idx)
        #         break
            else:
                df_1.to_csv(os.path.join(file_path, city + '_' + station_id + '.csv'), header=True, index=False)
                print('Data Saved')
                dummy_df = df_1

        except:

            sleep(60)
            driver.get('https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing/caaqm-data-availability')
            sleep(15)
            # Find the button using XPath and click it
            # Clearing previous details filled in each field
            button = driver.find_element_by_xpath('/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-availability/div/div/div/div/div/div/div[1]/div[1]/div/ng-select/div/div/div[2]')
            button.click()

            sleep(1)

            fill_data(field_name='state', value=state)
            sleep(1)
            fill_data(field_name='city', value=city)
            sleep(1)
            fill_data(field_name='station', value=station_name)
            sleep(1)

            # Find the button using XPath and click it
            button = driver.find_element_by_xpath('/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-availability/div/div/div/div/div/div/div[1]/div[4]/div/button')
            button.click()

            sleep(35)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find('table', {'class': 'table-hover'})

            headers = []
            rows = []
            for tr in table.tbody.find_all('tr'):
                row = []
                for td in tr.find_all('td'):
                    row.append(td.text.strip())
                rows.append(row)

            for th in table.thead.find_all('th'):
                headers.append(th.text.strip())

            df_1 = pd.DataFrame(rows, columns=headers)

            if df_1.equals(dummy_df):
                print("ERROR", end='\n\n')
                error_idx.append(idx)
        #         break
            else:
                df_1.to_csv(os.path.join(file_path, city + '_' + station_id + '.csv'), header=True, index=False)
                print('Data Saved')
                dummy_df = df_1
        
    
    
#     break
