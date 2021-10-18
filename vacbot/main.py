from logging import lastResort, log
from selenium import webdriver
import selenium
#from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.common.action_chains import ActionChains

import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from imap_tools import MailBox

import pandas as pd
arr = ["_Impfzentrum Triemli Zürich", "_Referenz-Impfzentrum Zürich", "Zürich, Amavita Apotheke Neumarkt Oerlikon","Zürich, Amavita Apotheke Zürich Altstetten", " Zürich, ApoDoc Hardbrücke (no appointment) "," Zürich, Apotheke Schaffhauserplatz","Zürich, Bahnhof Apotheke Oerlikon","Zürich, Coop Vitality Apotheke Zürich Bahnhofstrasse", " Zürich, DROPA Apotheke am Limmatplatz", "Zürich, Klus-Apotheke AG - Impfzentrum","Zürich, Medbase Apotheke Zürich Helvetiaplatz","Zürich, Neumarkt Apotheke","Zürich, Triemli-Apotheke & Drogerie"]


last_center=""
def main():

    login()


def select_app_caller(driver):
    
    while (select_appointment(driver) == False):
        driver.refresh()
        
        time.sleep(1)
        
    
def select_appointment( driver):
    global last_center
    selected = False  
    for i in range (3,79):
        try:
            loc = driver.find_element_by_xpath("/html/body/div/app-root/app-overview-page/app-overview/div/select/option["+str(i)+"]")
            
            if (loc.is_enabled()):

                if loc.text in arr and loc.text != last_center:
                    loc.click()
                    print("loc clicked", " ", loc.text)
                    selected = True
                    last_center = loc.text
                    break
                else:
                    continue
                #print("not enabled")
        except NoSuchElementException:
            print("no such element (appointment list)")
    return selected       

def extract_date(string):
    day = string.split(" ")
    month_num = day[1].split(".")[1]
    print(month_num)
    return month_num

def extract_day(string):
    day = string.split(" ")
    day_num = day[1].split(".")[0]
    print(day_num)
    return day_num

def login():
    user_agent = 'Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
   
    chrome_options = webdriver.ChromeOptions(); 
    chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument('--incognito')
    #chrome_options.add_argument("--disable-blink-features=AutomationControlled");
    chrome_options.add_argument(f'user-agent={user_agent}')
    #chrome_options.add_argument("window-size=1920,1080")
    #chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
    #chrome_options.add_experimental_option("detach", True)
    
    #driver.delete_all_cookies()
    driver = webdriver.Chrome( options=chrome_options)
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get("https://zh.vacme.ch/")
    time.sleep(1)
    if (driver.find_elements_by_xpath("/html/body/div[2]/div/div/div")):
         driver.get("https://zh.vacme.ch/auth/realms/vacme/protocol/openid-connect/auth?client_id=vacme-initial-app-prod&redirect_uri=https%3A%2F%2Fzh.vacme.ch%2Fstart&state=d385822f-9d38-403c-8e15-1fb68d47531f&response_mode=fragment&response_type=code&scope=openid&nonce=a4417e13-74ac-416a-bd60-af3a054ff3e2&code_challenge=U_snBwivOm4l5H49SaD-vpnU-05gtmMu1NBPQdhiOXo&code_challenge_method=S256")
         print("waiting room")
    username = driver._web_element_cls
    try:
        username = driver.find_element_by_id("username")
        username.send_keys("pierre.eichmeyer@gmail.com")
    except NoSuchElementException:
        
        login_but = driver.find_element_by_xpath("/html/body/div/app-root/app-landingpage/div/div[2]/p/a")
        
        
        login_but.click()
        username = driver.find_element_by_id("username")
        username.send_keys("pierre.eichmeyer@gmail.com")

    password = driver.find_element_by_id("password")
    
    password.send_keys("Architecte17/04")
    password.send_keys(Keys.RETURN)
    time.sleep(7)
    code = get_code()
    sms_code_field = driver.find_element_by_id("totp")
    sms_code_field.send_keys(code)
    sms_code_field.send_keys(Keys.RETURN)
    time.sleep(1)
    try:
        reg_but =  driver.find_element_by_id("vacme-branding")
        reg_but.click()
    except NoSuchElementException:
        print("already on correct page")
    
    select_app_caller(driver)
    select_app1(driver)  
    select_app2(driver)
    time.sleep(0.5)
    submit_button = driver.find_element_by_xpath("/html/body/div/app-root/app-overview-page/app-overview/div/lib-button/button")
    time.sleep(0.5)
    submit_button.click()
    print("submit clicked")
    if (driver.find_elements_by_class_name("swal2-popup swal2-modal swal2-icon-warning swal2-show")):
        driver.find_elements_by_class_name("swal2-popup swal2-modal swal2-icon-warning swal2-show").send_keys(Keys.ESCAPE)
    else:
        done = True  
    driver.close()
    driver.quit()

def select_app1(driver):
    notSelected1 = True
    while (notSelected1):
        time.sleep(10)
        if (driver.find_elements_by_class_name("swal2-popup swal2-modal swal2-icon-warning swal2-show")):
            driver.find_elements_by_class_name("swal2-popup swal2-modal swal2-icon-warning swal2-show").send_keys(Keys.ESCAPE)
            print("removed popup")
            select_app_caller(driver)
        else:
            app1_step1_select = driver.find_element_by_xpath("/html/body/div/app-root/app-overview-page/app-overview/div/lib-termin-overview-item[1]/div/div/div/button/img")
            app1_step1_select.click()
            print("selected app1 arrow")
            time.sleep(1)
            if (driver.find_elements_by_class_name("swal2-popup swal2-modal swal2-icon-warning swal2-show")):
                driver.find_elements_by_class_name("swal2-popup swal2-modal swal2-icon-warning swal2-show").send_keys(Keys.ESCAPE)
                print("removed popup")
                select_app_caller(driver)
            else:
                if (driver.find_elements_by_xpath("/html/body/div/app-root/app-terminfindung-page/div/lib-terminfindung/div/div[2]")):
                    time.sleep(1)
                    print("no hour app1")
                    back_but = driver.find_element_by_xpath("/html/body/div/app-root/div/lib-menu/nav/div[1]/a/div")
                    back_but.click()
                    print("pressed back button on app1")
                    select_app_caller(driver)
                else:
                    if (driver.find_elements_by_xpath("/html/body/div/app-root/app-terminfindung-page/div/lib-terminfindung/div/lib-date-spinner/div/b")):
                        date = driver.find_element_by_xpath("/html/body/div/app-root/app-terminfindung-page/div/lib-terminfindung/div/lib-date-spinner/div/b").text
                        if (extract_date(date) != "07" or int(extract_day(date)) >18):
                            back_but = driver.find_element_by_xpath("/html/body/div/app-root/div/lib-menu/nav/div[1]/a/div")
                            back_but.click()
                            print("pressed back button on app1")
                            select_app_caller(driver)
                        else:
                            back_but = driver.find_element_by_xpath("/html/body/div/app-root/div/lib-menu/nav/div[1]/a")
                            notSelected1 = False
                            print("selected hour app1")
                            back_but.send_keys(Keys.TAB*10 + Keys.RETURN)
                
            
            
        
            
    
    
def select_app2(driver):
    notSelected2 = True
    while(notSelected2):  
        try:
            app2_step1_select = driver.find_element_by_xpath("/html/body/div/app-root/app-overview-page/app-overview/div/lib-termin-overview-item[2]/div/div/div/button")
            app2_step1_select.click()
        except:
            continue
        print("now on page of app2 hour")
        if (driver.find_elements_by_class_name("swal2-popup swal2-modal swal2-icon-warning swal2-show")):
            driver.find_elements_by_class_name("swal2-popup swal2-modal swal2-icon-warning swal2-show").send_keys(Keys.ESCAPE)
            print("removed popup")
            select_app_caller(driver)
        try:
            time.sleep(1)
            app2_step2_select = driver.find_element_by_xpath("/html/body/div/app-root/app-terminfindung-page/div/lib-terminfindung/div/div/div[1]/lib-button/button")
            date = driver.find_element_by_xpath("/html/body/div/app-root/app-terminfindung-page/div/lib-terminfindung/div/lib-date-spinner/div/b")
            if ( int(extract_day(date.text))!= 13):
                            back_but = driver.find_element_by_xpath("/html/body/div/app-root/div/lib-menu/nav/div[1]/a/div")
                            back_but.click()
                            print("pressed back button on app1")
                            select_app_caller(driver)
            else:
                app2_step2_select.click()
                notSelected2 = False
                print("selected hour app2", notSelected2)
        except NoSuchElementException:
            back_but = driver.find_element_by_xpath("/html/body/div/app-root/app-terminfindung-page/div/a")
            back_but.click()
            print("no hour app2")
            select_app_caller(driver)
   

def get_code():    

    with MailBox('imap.gmail.com').login('darkcolonna@gmail.com', '2SbuHX9gPzZfgT') as mailbox:
        for msg in mailbox.fetch(limit=1, reverse=True):
            code = re.findall(r'\d+', msg.text)
        #mailbox.logout()
    return code.pop()
main()