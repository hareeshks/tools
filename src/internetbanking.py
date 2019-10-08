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


def test_internetbanking():
    # driver = webdriver.Chrome()
    driver.maximize_window()
    # driver.switch_to.window
    driver.get(
        "https://sibernet.southindianbank.com/corp/AuthenticationController?FORMSGROUP_ID__=AuthenticationFG&__START_TRAN_FLAG__=Y&FG_BUTTONS__=LOAD&ACTION.LOAD=Y&AuthenticationFG.LOGIN_FLAG=1&BANK_ID=059")

    wait_for(page_has_loaded)
    username = driver.find_element_by_xpath('//*[@id="AuthenticationFG.USER_PRINCIPAL"]')
    username.send_keys('username')

    password = driver.find_element_by_xpath('//*[@id="AuthenticationFG.ACCESS_CODE"]')
    password.send_keys('password')
    driver.find_element_by_xpath('//*[@id="VALIDATE_CREDENTIALS"]').click()
    driver.find_element_by_xpath('//*[@id="HREF_Logout"]').click()
    driver.find_element_by_xpath('//*[@id="HREF_Logout"]').click()
    '''
    end_time=time.time()
    exec_time=end_time-start_time
    print("Execution Time : " + str(exec_time))
    '''


def main():
    try:

        test_internetbanking()
        raise Exception
    except Exception as e:
        print("Errored : " + str(e))
        import requests
        urlskh = 'https://skh.ngdesk.com/ngdesk-rest/ngdesk/modules/5c9448b3b2039a000188774c/data?authentication_token='
        api_key = 'pdapikey'
        req_body = {"SUBJECT": "Internet banking failed", "MESSAGES": [{"MESSAGE": str(e), "ATTACHMENTS": []}],
                    "STATUS": "New", "REQUESTOR": "5c9448b3b2039a0001887754", "TEAMS": ["5c9448b3b2039a0001887756"],
                    "PRIORITY": "Critical", "ASSIGNEE": "5c9448b3b2039a0001887754"}
        print(req_body)
        r = requests.post(url=urlskh + api_key, data=str(req_body))
        # extracting response text  
        pastebin_url = r.text
        print("The pastebin URL is:%s" % pastebin_url)
        raise e


driver = webdriver.Remote(command_executor='http://127.0.0.1:4545/wd/hub',
                          desired_capabilities=DesiredCapabilities.CHROME)
#            desired_capabilities=DesiredCapabilities.INTERNETEXPLORER)
main()
