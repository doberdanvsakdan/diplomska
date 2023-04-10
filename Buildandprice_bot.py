from selenium import webdriver
from selenium.common import ElementNotInteractableException, NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re

from Product import Product

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

        prod1 = Product("C9200L-24P-4G-E", 1)
        prod2 = Product("C9200L-48P-4X-E", 2)
        prod3 = Product("C9300-24T-E", 3)
        prod4 = Product("C1000-24P-4G-L", 3)

        self.sez_products = [prod1,prod2,prod3,prod4]

    def login(self):
        #email = self.interact_with_element("userInput")
        email = self.browser.find_element(By.XPATH,'//*[@id="userInput"]')
        email.send_keys(usernameStr)

        nxt_btn = self.interact_with_element("login-button")
        nxt_btn.click()

        password = self.interact_with_element("okta-signin-password")
        self.send_key(password, passwordStr)

        nxt_btn = self.interact_with_element("okta-signin-submit")
        self.element_click(nxt_btn)
        #nxt_btn.click()

    def choose_estimate(self, create_new_estinate, estimate_name):
        if create_new_estinate:
            self.create_new_estimate()
        else:
            self.select_estimate(estimate_name)

    def create_new_estimate(self):
        time.sleep(4)
        create_new_btn = self.browser.find_elements(By.CLASS_NAME, 'createNewSubscription')
        create_new_btn[0].click()
        #Tuki smo zdej v novem oknu, kjer kreriramo estimate



        for st, product in enumerate(self.sez_products):
            self.add_product(product, st)

        time.sleep(100)

    def add_product(self, product, st):

        search_field = self.browser.find_element(By.ID, 'searchProd')
        search_field.send_keys(product.ime_produkta)

        element = self.interact_with_element("ui-id-1")
        self.element_click(element)
        add_btn = self.browser.find_element(By.ID, 'addProduct')
        add_btn.click()
        time.sleep(2)
        edit = self.browser.find_elements(By.CLASS_NAME, 'settingIcon')
        sez = []

        for el in edit:
            text = el.get_attribute("original-title")
            if text == "Edit Options":
                sez.append(el.get_attribute("id"))
        edit_btn = self.browser.find_element(By.ID, sez[st])
        edit_btn.click()
        self.edit_prod_spec(product)
        time.sleep(3)


    def edit_prod_spec(self, product):
        time.sleep(0.5)
        config_sez = ["Stack Module", "Secondary Power Supply", "Power Cables", "Console Cable", "Network PNP License"]

        #Dodaten napajalnik
        if product.dodaten_napajalnik:
            edit_btn = self.get_web_element(By.XPATH,'//*[@id="ullicontForNewCore"]/div/div/div/h6[3]/div/a')
            edit_btn.click()
            radio = self.get_web_element(By.XPATH, '/html/body/div[3]/div/div[16]/div[3]/div/div[17]/form/div[4]/table/tbody/tr/td[1]/label')
            self.element_click(radio)
            time.sleep(0.6)
        #Power cables
        edit_btn = self.get_web_element(By.XPATH,'//*[@id="ullicontForNewCore"]/div/div/div/h6[4]/div/a')
        self.element_click(edit_btn)
        radio = self.get_web_element(By.XPATH, '/html/body/div[3]/div/div[16]/div[3]/div/div[17]/form/div[1]/table/tbody/tr/td[1]/label')
        self.element_click(radio)
        time.sleep(0.5)
        if product.dodaten_napajalnik:
            edit_btn = self.get_web_element(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[1]/table/tbody/tr/td[3]/input')
            self.element_click(edit_btn)
            time.sleep(0.4)
            edit_btn.send_keys("2")

        #Done button
        edit_btn = self.get_web_element(By.XPATH,'//*[@id="sticky"]/div/div[2]/div[2]/div[3]/input[2]')
        self.element_click(edit_btn)
        time.sleep(2)
        edit_btn = self.get_web_element(By.XPATH, '//*[@id="sticky"]/div/div[2]/div[2]/div[3]/input[2]')
        self.element_click(edit_btn)
        time.sleep(0.8)

        #Confrm button
        edit_btn = self.get_web_element(By.XPATH, '//*[@id="doneModalBucket"]/div/form/div[6]/span/input')
        self.element_click(edit_btn)
        time.sleep(2)


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

    def get_web_element(self, By, identificator):
        element = None
        st = 0
        while (True):
            if st == 10: #2s
                break
            st+=1
            try:
                element = self.browser.find_element(By, identificator)
                break
            except ElementNotInteractableException as e:
                time.sleep(0.2)
            except NoSuchElementException as e:
                time.sleep(0.2)
        if element == None:
            print('Couldnt get element: {} by {}.'.format(identificator, By))
        return element

    #TODO: združi funkcijo "interact_with_element" in funkcijo "element_click". Naj dobi še en vhod, ki določi kaj se naredi s elementom
    def element_click(self, objct_to_click):
        if objct_to_click == None:
            print("Object to click is None Type")
            return False
        st = 0
        while (True):
            if st == 10: #2s
                break
            st+=1
            try:
                objct_to_click.click()
                return True
            except ElementNotInteractableException as e:
                time.sleep(0.2)
            except NoSuchElementException as e:
                time.sleep(0.2)
            except ElementClickInterceptedException as e :
                time.sleep(0.2)
            except StaleElementReferenceException as e:
                time.sleep(0.2)


    def send_key(self, element, string):
        while (True):
            try:
                element.send_keys(string)
                return True
            except ElementNotInteractableException as e:
                time.sleep(0.2)
            except NoSuchElementException as e:
                time.sleep(0.2)




def main ():
    create_new_estinate = True
    estimate_name = "ime_estimata"

    bot = BuildandpriceBot()
    bot.login()
    bot.choose_estimate(create_new_estinate, estimate_name)

    time.sleep(3)


if __name__ == '__main__':
    main()

