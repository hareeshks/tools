from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class DND:
    def get_dnd_status(number):
        url = "http://www.nccptrai.gov.in/nccpregistry/saveSearchSub.misc"
        title = "Telecom Commercial Communications Customer Preference Portal"
        status = 'unknown_error'
        try:
            driver = webdriver.Chrome()  # webdriver.Firefox()
            driver.get(url)
            assert title in driver.title
            phoneno = driver.find_element_by_name("phoneno")
            phoneno.clear()
            phoneno.send_keys(number)
            submit = driver.find_element_by_name("submit1")
            submit.click()
            reg_status = driver.find_element_by_css_selector("font").text
            status = True if reg_status == 'Registered' else False
            driver.close()
        except Exception as e:
            print(f"Error : {e}")
        return status
    # click css=font
    # assert "No results found." not in driver.page_source


def main():
    print(DND.get_dnd_status("4802893147"))


if __name__ == "__main__":
    main()
