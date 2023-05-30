from selenium import webdriver
from selenium.common import ElementNotInteractableException, NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        prod3 = Product("C9300-24T-E", 3) #TODO: ne dela
        prod4 = Product("C1000-24P-4G-L", 3)

        self.sez_products = [prod1,prod2,prod3,prod4]

    def login(self):
        #email = self.interact_with_element("userInput")
        email = self.browser.find_element(By.XPATH,'//*[@id="userInput"]')
        email.send_keys(usernameStr)


        self.element_click(By.ID, 'login-button')

        password = self.interact_with_element("okta-signin-password")
        self.send_key(password, passwordStr)

        self.element_click(By.ID, "okta-signin-submit")


    def choose_estimate(self, create_new_estinate, estimate_name):
        if create_new_estinate:
            self.create_new_estimate()
        else:
            self.select_estimate(estimate_name)

    def create_new_estimate(self):
        self.element_click(By.CLASS_NAME, 'createNewSubscription')
        #Tuki smo zdej v novem oknu, kjer kreriramo estimate



        for st, product in enumerate(self.sez_products):
            self.add_product(product, st)


    def add_product(self, product, st):

        search_field = self.browser.find_element(By.ID, 'searchProd')
        search_field.send_keys(product.ime_produkta)
        self.element_click(By.ID, "ui-id-1")
        self.element_click(By.ID, 'addProduct')

        self.element_click(By.LINK_TEXT, 'Edit Options')
        self.edit_prod_spec(product)


    #uredimo specifikacije produkta
    def edit_prod_spec(self, product):
        config_sez = ["Stack Module", "Secondary Power Supply", "Power Cables", "Console Cable", "Network PNP License"]

        #Dodaten napajalnik
        if product.dodaten_napajalnik:
            self.element_click(By.LINK_TEXT,'Secondary Power Supply')
            self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr/td[1]/label')
            time.sleep(0.5)

        #Power cables
        self.element_click(By.XPATH,'//*[@id="ullicontForNewCore"]/div/div/div/h6[4]/div/a')
        self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[1]/table/tbody/tr/td[1]/label')
        time.sleep(0.5)


        if product.dodaten_napajalnik: #ča imamo dodaten napajalnik potrebujemo dva kabla
            self.element_click(By.LINK_TEXT, 'Power Cables')

            qnt_inp = self.get_web_element(By.NAME, 'CAB-TA-EU')
            self.try_element_click(qnt_inp) #kliknemo, da pobriše prednastavljeno število 1
            qnt_inp.send_keys("2")
            time.sleep(0.6)
            self.element_click(By.LINK_TEXT, 'Console Cable') #mormo kliknit stran, da se shranita dva kabla
            time.sleep(0.6)

        #Done button
        self.element_click(By.XPATH,'//*[@id="tobe-capture"]/div[3]/div/div[14]/div[3]/div[2]/div[2]/div[3]/input[2]') #Todo: za vse te gumbe ne bom smeu uporabljat xpath, ker ne dela za vse produkte

        #Comfrm button
        btn = self.get_web_element(By.NAME, 'exitAddrAction')
        #self.element_click(By.XPATH, '//*[@id="doneModalBucket"]/div/form/div[5]/span/input')
        if self.try_element_click(btn) == False:
            print("elementa nismo mogli klikniti")
        time.sleep(1)

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
        try:
            element = WebDriverWait(self.browser, 8).until(
                EC.presence_of_element_located((By, identificator))
            )
        #except Exception as e:
         #   print(e)
        except:
            self.browser.quit()

        return element



    #TODO: združi funkcijo "interact_with_element" in funkcijo "element_click". Naj dobi še en vhod, ki določi kaj se naredi s elementom
    def element_click(self, By, identificator):
        #try:
        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.element_to_be_clickable((By, identificator))).click()
        #except Exception as e:
         #   print(e)
        #except:
         #   self.browser.quit()

        return True

    #stara funkcija za klikanje objektov
    def try_element_click(self, objct_to_click):
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
        return False



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


if __name__ == '__main__':
    main()

