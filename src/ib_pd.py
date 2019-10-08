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
    driver.get(
        "https://sibernet.southindianbank.com/corp/AuthenticationController?FORMSGROUP_ID__=AuthenticationFG&__START_TRAN_FLAG__=Y&FG_BUTTONS__=LOAD&ACTION.LOAD=Y&AuthenticationFG.LOGIN_FLAG=1&BANK_ID=059")

    wait_for(page_has_loaded)
    username = driver.find_element_by_xpath('//*[@id="AuthenticationFG.USER_PRINCIPAL"]')
    username.send_keys('username')

    password = driver.find_element_by_xpath('//*[@id="AuthenticationFG.ACCESS_CODE"]')
    password.send_keys('password')

    driver.find_element_by_xpath('//*[@id="VALIDATE_CREDENTIALS"]').click()
    name = driver.find_element_by_xpath('//*[@id="firstName"]').text
    print(name)
    driver.find_element_by_xpath('//*[@id="HREF_Logout"]').click()
    assert name == 'HAREESH KARAPPILL', 'Customer name validation failed'
    # HAREESH KARAPPILLY

    # driver.find_element_by_xpath('//*[@id="HREF_Logout"]').click()
    # driver.find_element_by_xpath('//*[@id="HREF_Lut"]').click()
    '''
    end_time=time.time()
    exec_time=end_time-start_time
    print("Execution Time : " + str(exec_time))
    '''


def main():
    try:

        test_internetbanking()
        # raise Exception
    except Exception as e:
        print("Errored : " + str(e))
        pager_ib(e)
        # pager_ib_session()
        raise e


def pager_ib(str_e):
    import requests
    api_version = '2'
    authorization_token = 'pukzc5Jrwxr5tyDyQeiM'
    headers = {
        'Authorization': 'Token token=' + authorization_token,
        'Accept': 'application/vnd.pagerduty+json;version=' + api_version,
        'Content-Type': "application/json",
        'From': 'hareeshks@sib.co.in'
    }
    payload = {"incident": {
        "type": "incident",
        "title": "The IB server is on fire.",
        "service": {
            "id": "PR6SUSE",
            "type": "service_reference"
        },
        "escalation_policy": {
            "id": "PHU7J6W",
            "type": "escalation_policy"
        },
        "body": {"type": "incident_body",
                 "details": str(str_e)}  #
    }
    }
    r = requests.get('https://api.pagerduty.com/services?time_zone=UTC&sort_by=name', headers=headers)
    print(r.text)
    r = requests.post('https://api.pagerduty.com/incidents', json=payload, headers=headers)
    print(r.text)
    print(r.status_code == 201)
    return


def pager_ib_session():
    import requests
    api_version = '2'
    authorization_token = 'pukzc5Jrwxr5tyDyQeiM'
    pagerduty_session = requests.Session()
    pagerduty_session.headers.update({
        'Authorization': 'Token token=' + authorization_token,
        'Accept': 'application/vnd.pagerduty+json;version=' + api_version,
        'Content-Type': "application/json",
    })

    payload = {
        "incident": {
            "type": "incident",
            "title": "Testing incident",
            "service": {
                "id": "PR6SUSE",
                "type": "service_reference"
            },
            "escalation_policy": {
                "id": "PHU7J6W",
                "type": "escalation_policy"
            }
        }
    }
    url = 'https://api.pagerduty.com/incidents'
    r = pagerduty_session.post(url, data=payload)
    print(r.text)
    return


driver = webdriver.Remote(command_executor='http://127.0.0.1:4545/wd/hub',
                          desired_capabilities=DesiredCapabilities.CHROME)
#            desired_capabilities=DesiredCapabilities.INTERNETEXPLORER)
# driver = webdriver.Chrome()
driver.maximize_window()
# driver.switch_to.window
main()
