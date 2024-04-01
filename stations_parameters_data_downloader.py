import os
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
# %config Completer.use_jedi=False

#     break

def next_month_(value):
    import datetime

    # Get the current date
    current_date = datetime.datetime.now()

    # Parse the given string to a date object
    given_date = datetime.datetime.strptime(value, '%B')

    # Add one month to the given date
    new_date = given_date.replace(year=current_date.year, month=(given_date.month%12)+1)

    # Get the month name of the new date
    month_name = new_date.strftime('%B')

#     print(month_name) # Output: 'July'
    return month_name


def fill_data(field_name, value):
    
    if field_name == 'state':
        field_box_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div[1]/div/ng-select/div/div/div[1]'
        field_box_text = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div[1]/div/ng-select/select-dropdown/div/div[1]/input'
        text = value
        
    elif field_name == 'city':
        field_box_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div[2]/div/ng-select/div/div/div[1]'
        field_box_text = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div[2]/div/ng-select/select-dropdown/div/div[1]/input'
        text = value
        
    elif field_name == 'station':
        field_box_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[1]/div/ng-select/div/div/div[1]'
        field_box_text = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[1]/div/ng-select/select-dropdown/div/div[1]/input'
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
        
def click_object(xpath):
    click_box = xpath
    click_box = driver.find_element_by_xpath(click_box)
    click_box.click()
    
df = pd.read_csv("./stations_details.csv")

driver = webdriver.Chrome('/usr/bin/chromedriver')
sleep(15)
# driver = webdriver.Firefox(executable_path="./geckodriver")

driver.get('https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing')
sleep(50)

root_dir = "./stations_data"
if not os.path.exists(root_dir):
    os.mkdir(root_dir)
    
for idx in range(len(df)):

    try:

        driver.get('https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing/data')
        sleep(5)

        state = df.state[idx]
        city = df.city[idx]
        station_id = df.id[idx]
        station_name = df.name[idx]
        start_month = df.start_month[idx][:3].upper()
        year = str(df.year[idx])

        print(f"{idx}. {state} :: {city} :: {station_id} :: {station_name} :: ", end='')


        file_path = os.path.join(root_dir, state)
        if not os.path.exists(file_path):
            os.mkdir(file_path)

        fill_data(field_name='state', value=state)
        sleep(1)
        fill_data(field_name='city', value=city)
        sleep(1)
        fill_data(field_name='station', value=station_name)
        sleep(1)

        parameters_box_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[1]/div/span[1]'
        click_object(parameters_box_click)
        sleep(1)

        select_all_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/div[1]/label/span[1]'
        click_object(select_all_click)
        sleep(1)

        blank_space_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[5]'
        click_object(blank_space_click)

        criteria_box_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[3]/div[2]/div/ng-select/div/div/div[1]'
        click_object(criteria_box_click)
        sleep(1)

        select_hr_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[3]/div[2]/div/ng-select/select-dropdown/div/div[2]/ul/li[3]'
        click_object(select_hr_click)
        sleep(1)

        ## from date
        from_date_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[1]/span'
        click_object(from_date_click)
        sleep(1)

        time_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[1]/div[4]/div'
        click_object(time_xpath)
        sleep(1)

        hr_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[1]/div[1]/input'
        click_object(hr_xpath)
        sleep(1)

        hr_text_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[1]/div[1]/input'
        hr_text_action = driver.find_element_by_xpath(hr_text_xpath)
        hr_text_action.clear()
        hr_text_action.send_keys('12')
        sleep(1)

        sec_text_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[1]/div[3]/input'
        sec_text_action = driver.find_element_by_xpath(sec_text_xpath)
        sec_text_action.clear()
        sec_text_action.send_keys('0')
        sleep(1)

        am_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[2]/div/button[1]'
        click_object(am_xpath)
        sleep(1)

        set_time_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[3]/button'
        click_object(set_time_xpath)
        sleep(1)

        month_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[2]/div'
        click_object(month_xpath)
        sleep(1)



        select_month = driver.find_element_by_id(start_month)
        select_month.click()
        sleep(1)

        year_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[3]/div'
        click_object(year_xpath)
        sleep(1)


        # find the select element by its name attribute
        select_element = driver.find_element_by_xpath('/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[3]')

        # create a new option element
        new_option = '<span _ngcontent-c6="" ng-reflect-ng-class="[object Object]" id="{0}">{0}</span>'.format(year)

        # execute a JavaScript code to add the new option element to the select element
        driver.execute_script("arguments[0].innerHTML += '{}'".format(new_option), select_element)
        sleep(1)

        select_year = driver.find_element_by_id(year)
        select_year.click()
        sleep(1)

        table_rows = driver.find_elements_by_xpath('/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/table[2]/tbody/tr[1]')
        pos_count = 0
        for i in table_rows:
            for j in i.text:
                if j.isdigit():
                    pos_count+=1
    #     pos_count

        exact_loc = 7 - pos_count + 1
    #     exact_loc

        day_xpath = f'/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/table[2]/tbody/tr[1]/td[{exact_loc}]/span'
        click_object(day_xpath)
        sleep(1)

        ## TO DATE


        to_date_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[1]/span'
        click_object(to_date_xpath)
        sleep(1)

        time_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/div[1]/div[4]/div'
        click_object(time_xpath)
        sleep(1)

        hr_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[1]/div[1]/input'
        click_object(hr_xpath)
        sleep(1)

        # hr_text_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[1]/div[1]/input'
        hr_text_action = driver.find_element_by_xpath(hr_xpath)
        hr_text_action.clear()
        hr_text_action.send_keys('12')
        sleep(1)

        sec_text_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[1]/div[3]/input'
        sec_text_action = driver.find_element_by_xpath(sec_text_xpath)
        sec_text_action.clear()
        sec_text_action.send_keys('0')
        sleep(1)

        am_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[2]/div/button[1]'
        click_object(am_xpath)
        sleep(1)

        set_time_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[3]/button'
        click_object(set_time_xpath)
        sleep(1)

        month_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/div[2]/div'
        click_object(month_xpath)
        sleep(1)

        # select_month = driver.find_element_by_id("DEC")
        # select_month.click()
        apr_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/div[4]/span[4]'
        click_object(apr_xpath)
        sleep(1)

        day_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/table[2]/tbody/tr[1]/td[7]/span'
        click_object(day_xpath)
        sleep(1)


        submit_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[5]/button'
        click_object(submit_click)
        sleep(25)



        # find the select element by its name attribute
        select_element = driver.find_element_by_xpath('/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data-report/div[2]/div[2]/div[1]/label/select')

        # create a new option element
        new_option = '<option value="5000">5000</option>'

        # execute a JavaScript code to add the new option element to the select element
        driver.execute_script("arguments[0].innerHTML += '{}'".format(new_option), select_element)
        sleep(1)

        dropdown_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data-report/div[2]/div[2]/div[1]/label/select'
        dropdown_click_action = driver.find_element_by_xpath(dropdown_click)
        dropdown_click_action.click()
        sleep(1)

        dropdown_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data-report/div[2]/div[2]/div[1]/label/select/option[5]'
        dropdown_click_action = driver.find_element_by_xpath(dropdown_click)
        dropdown_click_action.click()
        sleep(1)

        blank_space_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data-report/div[2]/div[2]'
        blank_space_click_action = driver.find_element_by_xpath(blank_space_click)
        blank_space_click_action.click()
        sleep(1)

        sleep(25)

        end_flag = 0
        while end_flag != 1:
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

            new_df = pd.DataFrame(rows, columns=headers)

            file_name = os.path.join(file_path, city + '_' + station_id + '.csv')

            if not os.path.exists(file_name):
                new_df.to_csv(file_name, header=True, index=False)
            else:
                old_df = pd.read_csv(file_name)
                if new_df.equals(old_df):
                    print("ERROR", end='\n\n')
                else:
                    old_df = old_df.append(new_df, ignore_index=True)
                    old_df.to_csv(file_name, header=True, index=False)
                    print('.', end='')


            #  Execute JavaScript code to scroll to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            try:
                # code that clicks the element that may cause ElementClickInterceptedException
                next_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data-report/div[2]/div[2]/div[4]/a[3]'
                next_click_action = driver.find_element_by_xpath(next_click)
                next_click_action.click()
                sleep(25)
            except ElementClickInterceptedException:
                print("COMPLETE")
                try:
                    del old_df, new_df
                except:
                    pass
                end_flag = 1

    except:
        sleep(30)
        driver.get('https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing/data')
        sleep(30)

        state = df.state[idx]
        city = df.city[idx]
        station_id = df.id[idx]
        station_name = df.name[idx]
        start_month = next_month_(df.start_month[idx])[:3].upper()
        year = str(df.year[idx])

        print(f"{idx}. {state} :: {city} :: {station_id} :: {station_name} :: ", end='')

        file_path = os.path.join(root_dir, state)
        if not os.path.exists(file_path):
            os.mkdir(file_path)

        fill_data(field_name='state', value=state)
        sleep(1)
        fill_data(field_name='city', value=city)
        sleep(1)
        fill_data(field_name='station', value=station_name)
        sleep(1)

        parameters_box_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[1]/div/span[1]'
        click_object(parameters_box_click)
        sleep(1)

        select_all_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/div[1]/label/span[1]'
        click_object(select_all_click)
        sleep(1)

        blank_space_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[5]'
        click_object(blank_space_click)

        criteria_box_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[3]/div[2]/div/ng-select/div/div/div[1]'
        click_object(criteria_box_click)
        sleep(1)

        select_hr_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[3]/div[2]/div/ng-select/select-dropdown/div/div[2]/ul/li[3]'
        click_object(select_hr_click)
        sleep(1)

        ## from date
        from_date_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[1]/span'
        click_object(from_date_click)
        sleep(1)

        time_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[1]/div[4]/div'
        click_object(time_xpath)
        sleep(1)

        hr_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[1]/div[1]/input'
        click_object(hr_xpath)
        sleep(1)

        hr_text_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[1]/div[1]/input'
        hr_text_action = driver.find_element_by_xpath(hr_text_xpath)
        hr_text_action.clear()
        hr_text_action.send_keys('12')
        sleep(1)

        sec_text_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[1]/div[3]/input'
        sec_text_action = driver.find_element_by_xpath(sec_text_xpath)
        sec_text_action.clear()
        sec_text_action.send_keys('0')
        sleep(1)

        am_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[2]/div/button[1]'
        click_object(am_xpath)
        sleep(1)

        set_time_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[3]/button'
        click_object(set_time_xpath)
        sleep(1)

        month_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[2]/div'
        click_object(month_xpath)
        sleep(1)

        select_month = driver.find_element_by_id(start_month)
        select_month.click()
        sleep(1)

        year_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[3]/div'
        click_object(year_xpath)
        sleep(1)

        # find the select element by its name attribute
        select_element = driver.find_element_by_xpath(
            '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[3]')

        # create a new option element
        new_option = '<span _ngcontent-c6="" ng-reflect-ng-class="[object Object]" id="{0}">{0}</span>'.format(year)

        # execute a JavaScript code to add the new option element to the select element
        driver.execute_script("arguments[0].innerHTML += '{}'".format(new_option), select_element)
        sleep(1)

        select_year = driver.find_element_by_id(year)
        select_year.click()
        sleep(1)

        table_rows = driver.find_elements_by_xpath(
            '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/table[2]/tbody/tr[1]')
        pos_count = 0
        for i in table_rows:
            for j in i.text:
                if j.isdigit():
                    pos_count += 1
        #     pos_count

        exact_loc = 7 - pos_count + 1
        #     exact_loc

        day_xpath = f'/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/table[2]/tbody/tr[1]/td[{exact_loc}]/span'
        click_object(day_xpath)
        sleep(1)

        ## TO DATE

        to_date_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[1]/span'
        click_object(to_date_xpath)
        sleep(1)

        time_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/div[1]/div[4]/div'
        click_object(time_xpath)
        sleep(1)

        hr_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[1]/div[1]/input'
        click_object(hr_xpath)
        sleep(1)

        # hr_text_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[1]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[1]/div[1]/input'
        hr_text_action = driver.find_element_by_xpath(hr_xpath)
        hr_text_action.clear()
        hr_text_action.send_keys('12')
        sleep(1)

        sec_text_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[1]/div[3]/input'
        sec_text_action = driver.find_element_by_xpath(sec_text_xpath)
        sec_text_action.clear()
        sec_text_action.send_keys('0')
        sleep(1)

        am_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[2]/div/button[1]'
        click_object(am_xpath)
        sleep(1)

        set_time_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/div[5]/div[3]/button'
        click_object(set_time_xpath)
        sleep(1)

        month_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/div[2]/div'
        click_object(month_xpath)
        sleep(1)

        # select_month = driver.find_element_by_id("DEC")
        # select_month.click()
        apr_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/div[4]/span[4]'
        click_object(apr_xpath)
        sleep(1)

        day_xpath = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[4]/div[2]/div/div/div/angular2-date-picker/div/div[2]/table[2]/tbody/tr[1]/td[7]/span'
        click_object(day_xpath)
        sleep(1)

        submit_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[5]/button'
        click_object(submit_click)
        sleep(25)

        # find the select element by its name attribute
        select_element = driver.find_element_by_xpath(
            '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data-report/div[2]/div[2]/div[1]/label/select')

        # create a new option element
        new_option = '<option value="5000">5000</option>'

        # execute a JavaScript code to add the new option element to the select element
        driver.execute_script("arguments[0].innerHTML += '{}'".format(new_option), select_element)
        sleep(1)

        dropdown_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data-report/div[2]/div[2]/div[1]/label/select'
        dropdown_click_action = driver.find_element_by_xpath(dropdown_click)
        dropdown_click_action.click()
        sleep(1)

        dropdown_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data-report/div[2]/div[2]/div[1]/label/select/option[5]'
        dropdown_click_action = driver.find_element_by_xpath(dropdown_click)
        dropdown_click_action.click()
        sleep(1)

        blank_space_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data-report/div[2]/div[2]'
        blank_space_click_action = driver.find_element_by_xpath(blank_space_click)
        blank_space_click_action.click()
        sleep(1)

        sleep(25)

        end_flag = 0
        while end_flag != 1:
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

            new_df = pd.DataFrame(rows, columns=headers)

            file_name = os.path.join(file_path, city + '_' + station_id + '.csv')

            if not os.path.exists(file_name):
                new_df.to_csv(file_name, header=True, index=False)
            else:
                old_df = pd.read_csv(file_name)
                if new_df.equals(old_df):
                    print("ERROR", end='\n\n')
                else:
                    old_df = old_df.append(new_df, ignore_index=True)
                    old_df.to_csv(file_name, header=True, index=False)
                    print('.', end='')

            #  Execute JavaScript code to scroll to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            try:
                # code that clicks the element that may cause ElementClickInterceptedException
                next_click = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data-report/div[2]/div[2]/div[4]/a[3]'
                next_click_action = driver.find_element_by_xpath(next_click)
                next_click_action.click()
                sleep(25)
            except ElementClickInterceptedException:
                print("COMPLETE")
                try:
                    del old_df, new_df
                except:
                    pass
                end_flag = 1

#     break
    
