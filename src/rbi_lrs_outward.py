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
driver.get("https://secweb.rbi.org.in/orfsxbrl/customer/index.jsp")

wait_for(page_has_loaded)
username = driver.find_element_by_xpath('//*[@id="userName"]')
username.send_keys('username')

password = driver.find_element_by_xpath('//*[@id="password"]')
password.send_keys('password')

bank_code = driver.find_element_by_xpath('//*[@id="bankCode"]')
driver.execute_script('document.getElementsByName("bankCode")[0].removeAttribute("readonly")')
bank_code.clear()
bank_code.send_keys('bankcode')
wait_for(page_has_loaded)
captcha = driver.find_element_by_xpath('//*[@id="capchaCode"]')
captchatext = ""

for i in range(1, 7, 1):
    captchatext += str(driver.find_element_by_xpath('//*[@id="c' + str(i) + '"]').text.strip())

captcha.send_keys(captchatext)

driver.find_element_by_xpath('//input[@value=\'Submit\']').click()

driver.find_element_by_link_text('LRS Status of Remitter').click()
pan = driver.find_element_by_xpath('//*[@id="pan"]')
pan_value = 'PANOFCUSTOMER'
pan.send_keys(pan_value)

# period=driver.find_element_by_xpath('//*[@id="period"]')
period = driver.find_element_by_xpath('//*[@id="period"]')

driver.execute_script('document.getElementById(\'period\').removeAttribute("readonly")')
# period.click()

period.send_keys('27-FEB-2019')
driver.execute_script('return fetchRec();')

wait_for(page_has_loaded)
wait_for(page_has_loaded)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[text()='" + pan_value + "']")))
finally:
    # time.sleep(100)
    row_count = len(driver.find_elements_by_xpath("//td[text()='" + pan_value + "']")) + 1
    total_amount = driver.find_element_by_xpath(
        '//*[@id="local"]/div/table/tbody/tr[' + str(row_count) + ']/td[2]/b').text
    print(pan_value + ' Total Amount :' + str(total_amount))

driver.find_element_by_xpath('//*[@id="ctl00_Top1_btnLogOut"]').click()

end_time = time.time()
exec_time = end_time - start_time
print("Execution Time : " + str(exec_time))
