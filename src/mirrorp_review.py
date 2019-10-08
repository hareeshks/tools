# https://secweb.rbi.org.in/orfsxbrl
# java -jar selenium-server-standalone-3.141.59.jar -port 4545
# -Dwebdriver.chrome.driver=./chromedriver
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import csv

start_time = time.time()


def page_has_loaded():
    page_state = driver.execute_script(
        'return document.readyState;'
    )
    return page_state == 'complete'


def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 3:
        if condition_function():
            return True
        else:
            time.sleep(1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )


driver = webdriver.Remote(command_executor='http://127.0.0.1:4545/wd/hub',
                          desired_capabilities=DesiredCapabilities.CHROME)
#            desired_capabilities=DesiredCapabilities.INTERNETEXPLORER)
# driver = webdriver.Chrome()
driver.maximize_window()
# driver.switch_to.window
driver.get("https://play.google.com/apps/publish/")

wait_for(page_has_loaded)
username = driver.find_element_by_xpath('//*[@id="identifierId"]')
username.send_keys('gmail_username')
username.send_keys(Keys.RETURN)
wait_for(page_has_loaded)
time.sleep(5)
password = driver.find_element_by_xpath("//input[@name='password']")
password.send_keys('gmail_password')

password.send_keys(Keys.RETURN);

time.sleep(10)

wait_for(page_has_loaded)

# with open('reviews_reviews_com.SIBMobile_201905.csv') as csv_file:
input_file = 'reviews_reviews_com.SIBMobile_201907.csv'
data = ''
with open(input_file, 'r') as file:
    data = file.read()
rawdata = data.strip()
file.close()
# print(rawdata)
myreader = csv.DictReader(rawdata.splitlines())
writehead = [list_word for list_word in myreader.fieldnames]
writehead.append('CustomerName')
w = open(input_file + '_mod.txt', 'w')
writer = csv.DictWriter(w, delimiter=',', fieldnames=writehead)
writer.writeheader()
for row in myreader:
    print(row['ReviewLink'])
    if row['ReviewLink'] and row['StarRating'] == '1':
        driver.get(str(row['ReviewLink']))

        wait_for(page_has_loaded)
        time.sleep(15)
        name = driver.find_element_by_css_selector('span > strong:nth-child(1)')
        name = name.text.replace(',', ' ')
        print(name)
        row['CustomerName'] = name
    else:
        row['CustomerName'] = ''
    print(row)
    writer.writerow(row)

w.close()
driver.find_element_by_xpath('//*[@id="gwt-uid-24"]').click()
driver.find_element_by_xpath('//*[@id="gwt-uid-26"]').click()

w.close

end_time = time.time()
exec_time = end_time - start_time
print("Execution Time : " + str(exec_time))
