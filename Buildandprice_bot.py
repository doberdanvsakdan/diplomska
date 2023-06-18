
from selenium import webdriver
from selenium.common import ElementNotInteractableException, NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException, TimeoutException, ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


from Product import Product

usernameStr = 'sergej.asic@snt.si'
passwordStr = 'tporeco2014HD'

terka_exeptionov = [ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException]

class BuildandpriceBot:
    def __init__(self, product_dict):
        self.browser = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        #self.browser.fullscreen_window()
        self.browser.set_window_position(0, 0)
        self.browser.set_window_size(1920, 1080)
        self.browser.get(('https://apps.cisco.com/Commerce/estimate'))

        self.product_dict = product_dict

    def login(self):
        #email = self.get_web_element(By.ID,'userInput')
        #email.send_keys(usernameStr)
        self.send_keys(By.ID,'userInput', usernameStr)

        self.element_click(By.ID, 'login-button')
        time.sleep(1)
        self.send_keys(By.ID, "okta-signin-password", passwordStr, 6)

        log_in_btn = self.get_web_element(By.ID, "okta-signin-submit")
        self.try_element_click(log_in_btn)
        #self.element_click(By.ID, "okta-signin-submit")


    def choose_estimate(self, create_new_estinate, estimate_name):
        self.element_click(By.ID, 'onetrust-reject-all-handler') #sprejmemo/zavrnemo piškotke
        if create_new_estinate:
            self.create_new_estimate()
        else:
            self.select_estimate(estimate_name)

    def create_new_estimate(self):
        time.sleep(0.8)
        self.element_click(By.CLASS_NAME, 'createNewSubscription', 20)

        #Tuki smo zdej v novem oknu, kjer kreriramo estimate
        for key in (self.product_dict):
            self.add_product(self.product_dict[key])

    def select_estimate(self, estimate_name):
        self.element_click(By.LINK_TEXT, estimate_name,5)

        #To je zaenkrat zgolj zaradi testiranja
        prod1 = Product("C9200L-24P-4G-E", 1)

        # urejanje Servicev - PRST
        edit_service = self.get_web_elements(By.LINK_TEXT, 'Edit Service/Subscription')
        sez_services = []
        for i in range(len(edit_service) - 1):
            sez_services.append(edit_service[i])

        #if self.try_element_click(edit_service[len(edit_service) - 1]):
         #   self.edit_prod_services(prod1)

    def add_product(self, product):
        search_field = self.get_web_element(By.ID, 'searchProd')
        search_field.send_keys(product.ime_produkta)
        print(f'Adding product: {product.ime_produkta}.')
        self.element_click(By.ID, 'addProduct', 8)
        time.sleep(1)

        #da urejamo zadnji dodani produkt
        edit_options = self.get_web_elements(By.CLASS_NAME, 'spanBorder')
        sez = []
        for i in range(len(edit_options)-1):
            if edit_options[i].text == "Edit Options":
                sez.append(edit_options[i])

        if self.try_element_click(sez[len(sez)-1]):
            self.edit_prod_spec(product)

        #urejanje Servicev - PRST
        edit_service = self.get_web_elements(By.LINK_TEXT, 'Edit Service/Subscription')
        sez_services = []
        for i in range(len(edit_service)-1):
            sez_services.append(edit_service[i])

        #if self.try_element_click(edit_service[len(edit_service)-1]):
         #   self.edit_prod_services(product)


    #uredimo specifikacije produkta
    def edit_prod_spec(self, product):
        time.sleep(1)


        #da dobimo vse možnosti za urejanje specifikacije
        sez =self.get_web_elements(By.CLASS_NAME, 'renderNewClass')
        config_web_elements = []
        #config_sez = ["DNA", "Network Module", "Stack Module", "Primary Power Supply", "Secondary Power Supply", "Power Cables", "Storage Module", "Network PNP License", "Console Cable", "StackWise Cables", "Stack Power Cables"]
        for el in sez:
            config_web_elements.append(el.accessible_name)

        #DNA licenca - leta
        if 'DNA On-Prem Subscription' in config_web_elements or 'DNAC On-Prem Subscription' in config_web_elements:
            buttons = self.get_web_elements(By.CLASS_NAME, 'navigationselection')
            for el in buttons:
                if el.text.__contains__('DNA'):
                    self.try_element_click(el)
                    break
            # TODO: to verjetno dela samo za en specifičen produkt. Če ima kdo drugačno postavitev divov ne bo delalo?
            if product.dna_lic == 3:
                self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/div/div[2]/table/tbody/tr[1]/td[1]/label')
            if product.dna_lic == 5:
                self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/div/div[2]/table/tbody/tr[2]/td[1]/label')
            if product.dna_lic == 7:
                self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/div/div[2]/table/tbody/tr[3]/td[1]/label')

        time.sleep(1)
        self.browser.execute_script("window.scrollTo(0, 720)")



        #Stack modul
        if 'Stack Module' in config_web_elements:
            if product.dodatni_stack_kabli:
                self.element_click(By.LINK_TEXT, 'Stack Module')
                self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr/td[1]/label')
                self.browser.execute_script("window.scrollTo(0, 720)")


        #Dodaten napajalnik
        if 'Secondary Power Supply' in config_web_elements:
            if product.dodaten_napajalnik:
                if self.element_click(By.LINK_TEXT, 'Secondary Power Supply') == None: #nevem zakaj samo pri c9300 ne gre kliknit Scnd Pwr Sply z link textom, čeprav obstaja
                    elements = self.get_web_elements(By.CLASS_NAME, 'renderNewClass')
                    for el in elements:
                        if el.get_attribute('kdfid') == 'link_SecondaryPowerSupply':
                            self.try_element_click(el)
                            break
                self.browser.execute_script("window.scrollTo(0, 720)")
                time.sleep(0.5)
                sez_napajalnikov = self.get_web_elements(By.CLASS_NAME, 'skutitle')
                if sez_napajalnikov != None and len(sez_napajalnikov) > 1:
                    if product.scnd_pwr_sply == "brez":
                        self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[1]/td[1]/label')
                    if product.scnd_pwr_sply == "350wac":
                        self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[2]/td[1]/label')
                    if product.scnd_pwr_sply == "715wac":
                        self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[3]/td[1]/label')
                    if product.scnd_pwr_sply == "1100wac":
                        self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[4]/td[1]/label')
                    if product.scnd_pwr_sply == "715wdc":
                        self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[5]/td[1]/label')
                else:
                    self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr/td[1]/label') #radio button
                time.sleep(0.1)

        #Power cables
        self.element_click(By.LINK_TEXT,'Power Cables')
        self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[1]/table/tbody/tr/td[1]/label')
        time.sleep(0.5)

        if product.dodaten_napajalnik and 'Secondary Power Supply' in config_web_elements: #ča imamo dodaten napajalnik potrebujemo dva kabla
            self.element_click(By.LINK_TEXT, 'Power Cables')

            qnt_inp = self.get_web_element(By.NAME, 'CAB-TA-EU')
            self.try_element_click(qnt_inp) #kliknemo, da pobriše prednastavljeno število 1
            self.element_click(By.NAME, 'CAB-TA-EU')
            qnt_inp.send_keys("2")
            time.sleep(0.2)
            self.element_click(By.LINK_TEXT, 'Secondary Power Supply') #mormo kliknit stran, da se shranita dva kabla
            time.sleep(0.1)
            self.browser.execute_script("window.scrollTo(0, 720)")

        #Console cable
        if 'Console Cable' in config_web_elements:
            if self.element_click(By.LINK_TEXT, 'Console Cable') == None:
                self.element_click(By.LINK_TEXT, 'Console Cables') #nekatera stikala imajo Console Cables namesto Console Cable
            if product.console_cab == 'RJ45':
                strazar = self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[2]/td[1]/label',1)
                if strazar == None: #to mamo, če je samo 1 element - npr. pri c9100
                    self.element_click(By.XPATH,'//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[1]/td[1]/label')
            if product.console_cab == 'USB':
                self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[1]/td[1]/label')

        self.browser.execute_script("window.scrollTo(0, 720)")
        #Network modul
        if 'Network Module' in config_web_elements:
            if self.element_click(By.LINK_TEXT, 'Network Module'):
                if product.network_modul == "4X":
                    self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[1]/td[1]/label')
                if product.network_modul == "4G":
                    self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[2]/td[1]/label')
                if product.network_modul == 'brez':
                    self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[3]/td[1]/label')

        #Storage module
        if 'Storage Module' in config_web_elements:
            self.element_click(By.LINK_TEXT, 'Storage Module')
            if product.storage_module == "brez":
                self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[1]/td[1]/label')
            if product.storage_module == "240g":
                self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[2]/td[1]/label')

        #Stack power cables
        if 'Stack Power Cables' in config_web_elements:
            self.element_click(By.LINK_TEXT, 'Stack Power Cables')
            if product.stack_pwr_cables == "30cm":
                self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[1]/td[1]/label')
            if product.stack_pwr_cables == "150cm":
                self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[2]/td[1]/label')
            if product.stack_pwr_cables == "brez":
                self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[3]/td[1]/label')

        #StackWise Cable
        if 'StackWise Cable' in config_web_elements:
            self.element_click(By.LINK_TEXT, 'StackWise Cable')
            if product.stack_wise_cable == "50cm":
                self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[1]/td[1]/label')
            if product.stack_wise_cable == "1m":
                self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[2]/td[1]/label')
            if product.stack_wise_cable == "3m":
                self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[3]/td[1]/label')
            if product.stack_wise_cable == "brez":
                self.element_click(By.XPATH, '//*[@id="icwConfigOptions"]/form/div[4]/table/tbody/tr[4]/td[1]/label')

        #Done button
        #self.element_click(By.XPATH,'//*[@id="tobe-capture"]/div[3]/div/div[14]/div[3]/div[2]/div[2]/div[3]/input[2]')
        buttons = self.browser.find_elements(By.CLASS_NAME, 'tooltipSe')
        for button in buttons:
            if button.accessible_name == "Done":
                self.browser.execute_script("arguments[0].click();", button)
                break


        #Comfrm button
        time.sleep(1)
        buttons = self.browser.find_elements(By.CLASS_NAME, 'icwFinalButtonDone')
        for button in buttons:
            if button.accessible_name == "Done":
                self.browser.execute_script("arguments[0].click();", button)
                print(f'Done editing product: {product.ime_produkta}.\n')
                break
        time.sleep(0.3)

    def edit_prod_services(self, product):
        print(f'Editing Service/Subscription for product {product.ime_produkta}.')
        time.sleep(0.5)
        self.element_click(By.LINK_TEXT, 'Service', 10)

        input_service = self.get_web_elements(By.CLASS_NAME, 'choose-result-input')
        input_service[1].clear()
        self.send_key(input_service[1], product.tip_podpore)
        self.send_key(input_service[1], Keys.ENTER)
        time.sleep(0.5)

        inputs = self.get_web_elements(By.CLASS_NAME, 'form-control')
        for input in inputs:
            if input.accessible_name == 'Months: 1 to 84':
                str_podpore = str(product.let_podpore * 12)
                self.send_key(input, str_podpore)
                time.sleep(0.15)
                break

        apply_buttons = self.get_web_elements(By.CLASS_NAME, 'pull-right')
        for button in apply_buttons:
            if button.accessible_name == "Apply":
                self.try_element_click(button)
                break

        done_buttons = self.get_web_elements(By.CLASS_NAME, 'service-done-button')
        for button in done_buttons:
            if button.accessible_name == "Done":
                self.try_element_click(button)
                break
        print(f'Done editing Service/Subscription for product {product.ime_produkta}.')




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
            element = WebDriverWait(self.browser, 10, 0.5, terka_exeptionov).until(
                EC.presence_of_element_located((By, identificator)))
        except:
            print(f'Error in get_web_element. "{identificator}" by locator "{By}".')

        return element

    def get_web_elements(self, By, identificator, num_of_tries=2):
        elements = None
        st = 1
        while st <= num_of_tries:
            try:
                elements = WebDriverWait(self.browser, 4, 0.5, terka_exeptionov).until(
                    EC.presence_of_all_elements_located((By, identificator)))
                break
            except Exception as e:
                print(e)
                print(f'Error in get_web_elements. "{identificator}" by locator "{By}". Number of tryes: {st}')
            st+=1

        return elements
    def send_keys(self, By, identificator, string, num_of_tries=2):
        element = None
        st = 1
        while st <= num_of_tries:
            try:
                element = WebDriverWait(self.browser, 4, 0.5, terka_exeptionov).until(
                    EC.visibility_of_element_located((By, identificator)))
                if element:
                    element.send_keys(string)
                    break
            except:
                print(f'Cannot send keys. "{identificator}" by locator "{By}". Number of tryes: {st}')
            st+=1
    #sprejme objekekt kateremu želi poslati key-s
    def send_key(self, objct_to_send_keys, string):
        if objct_to_send_keys == None:
            print(f'Object to click is None Type. Cannot send key: {string}.')
            return False
        st = 0
        while (True):
            if st == 10:  # 2s
                break
            st += 1
            try:
                objct_to_send_keys.send_keys(string)
                return True
            except ElementNotInteractableException as e:
                time.sleep(0.2)
            except NoSuchElementException as e:
                time.sleep(0.2)
            except ElementClickInterceptedException as e:
                time.sleep(0.2)
            except StaleElementReferenceException as e:
                time.sleep(0.2)
        print(f'Cannot send key: {string}.')
        return False


    def element_click(self, By, identificator, num_of_tries=3):
        time.sleep(0.2)
        st = 1
        while st <= num_of_tries:
            try:
                element = WebDriverWait(self.browser, 4, 0.5, terka_exeptionov).until(EC.visibility_of_element_located((By, identificator)))
                if element:
                    element_to_click = WebDriverWait(self.browser, 5, 0.2, terka_exeptionov).until(EC.element_to_be_clickable((By, identificator)))
                    if element_to_click:
                        element_to_click.click()
                        return element
                    else:
                        print("Cannot click element.")

            except TimeoutException as e:
                print(f'Cannot locate element. Timeout Exeption: at element "{identificator}" by locator "{By}". Number of tries: {st}')
                #print(e)

            except ElementClickInterceptedException as e:
                print(f'Cannot locate element. ElementClick Intercepted Exception: at element "{identificator}" by locator "{By}". Number of tries: {st} ')

            st+=1
        time.sleep(0.1)
        return None


    #stara funkcija za klikanje objektov
    def try_element_click(self, objct_to_click):
        if objct_to_click == None:
            print("Object to click is None Type. Cannot locate element.")
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






def main (product_dict, run_with_gui=False):
    create_new_estinate = True
    estimate_name = "Estimate_BK144951854RO"


    bot = BuildandpriceBot(product_dict)
    bot.login()
    bot.choose_estimate(create_new_estinate, estimate_name)
    print("Program done running configuration.")
    time.sleep(10)





    #prod3 = Product("C9300-24T-E", 3)  # TODO: ne dela
    #prod4 = Product("C1000-24P-4G-L", 4)
prod1 = Product("C9200-24P-E", 0) # pri tem se lahko izbira network modul
prod2 = Product("C9200L-24P-4G-E", 1) #ima vgrajen network modul, in ga ne moreš zbirati
prod3 = Product("C9300-24T-E", 2)
prod4 = Product("C9200-48P-E", 3)
prod5 = Product("C1000-24P-4G-L", 4)
prod6 = Product("C9120AXI-E", 5)
product_dict = {}
sez = [prod6]
for st, produkt in enumerate(sez):
    product_dict[st] = produkt
print()
if __name__ == '__main__':
    main(product_dict)




