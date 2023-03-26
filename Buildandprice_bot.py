from selenium import webdriver
from selenium.common import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re

usernameStr = 'sergej.asic@snt.si'
passwordStr = 'tporeco2014HD'

class BuildandpriceBot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-extensions')
        #chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
        #self.browser.set_window_position(0, 0)

        #self.browser.set_window_size(1920, 1080)
        self.browser.get(('https://apps.cisco.com/Commerce/estimate'))

    def login(self):
        email = self.interact_with_element("userInput")
        email.send_keys(usernameStr)

        nxt_btn = self.interact_with_element("login-button")
        nxt_btn.click()

        password = self.interact_with_element("okta-signin-password")
        password.send_keys(passwordStr)

        nxt_btn = self.interact_with_element("okta-signin-submit")
        self.element_click(nxt_btn)
        nxt_btn.click()

    def choose_estimate(self, create_new_estinate, estimate_name):
        if create_new_estinate:
            self.create_new_estimate()
        else:
            self.select_estimate(estimate_name)

    def create_new_estimate(self):
        create_new_btn = self.browser.find_element(By.ID, 'contentHeaderCreateEstimate')
        create_new_btn.click()

        time.sleep(100)

    def select_estimate(self, estimate_name):
        pass

    #gets element by id
    #function needed to wait for the page to load
    def interact_with_element(self, id):
        element = None
        while(True):
            try:
                element = self.browser.find_element(By.ID, id)
                break
            except ElementNotInteractableException as e:
                time.sleep(0.2)
            except NoSuchElementException as e:
                time.sleep(0.2)
        return element

    #TODO: združi funkcijo "interact_with_element" in funkcijo "element_click". Naj dobi še en vhod, ki določi kaj se naredi s elementom
    def element_click(self, nxt_btn):
        while (True):
            try:
                nxt_btn.click()
                return True
            except ElementNotInteractableException as e:
                time.sleep(0.2)
            except NoSuchElementException as e:
                time.sleep(0.2)
        return False


def main ():
    create_new_estinate = True
    estimate_name = "ime_estimata"

    bot = BuildandpriceBot()
    bot.login()
    time.sleep(100)
    bot.choose_estimate(create_new_estinate, estimate_name)

    time.sleep(3)


if __name__ == '__main__':
    main()