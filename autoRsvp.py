from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from time import sleep

ATTEND_BUTTON_XPATH = "//*[@data-testid='attend-irl-btn']"
WAITLIST_BUTTON_XPATH = "//*[@data-testid='waitlist-btn']"
PAY_ORGANISER_XPATH = "/html/body/div[1]/div[3]/div/div[1]/div/div/div/div/div[2]/div[3]/button"
JOIN_WAITLIST_WITH_LOW_PRIO_XPATH = "/html/body/div[1]/div[3]/div/div[1]/div/div/div/div[1]/div/button"
MEETUP_URL = "https://www.meetup.com"


class Autorsvp():
    def __init__(self,email,password):
    
        self.browser = webdriver.Chrome()
        self.browser.get(MEETUP_URL)

        self.email = email
        self.password = password
    
    def login_with_email(self):
        
        sleep(2)

        login_button = self.browser.find_element(By.XPATH,'//*[@id="login-link"]')
        login_button.click()
        
        sleep(1)

        email_box = self.browser.find_element(By.ID,"email")
        email_box.send_keys(self.email)

        sleep(1)

        password_box = self.browser.find_element(By.ID,"current-password")
        password_box.send_keys(self.password)
        
        sleep(1)

        login_button = self.browser.find_element(By.NAME,"submitButton")
        login_button.click()

        print("logging in...")

        sleep(1)



    def rsvp_meeting(self,link):
        self.browser.get(link)
        
        #If Already RSVP'ed

        # if self.__check_already_going():
        # 	return

        #Click RSVP Button

        if self.browser:
            print("got browser")
        sleep(5)

        attend_button = self.find_element_by_xpath(ATTEND_BUTTON_XPATH)
        if attend_button:
            print("attending event")
            attend_button.click()
            sleep(5)

            self.click_elem_by_xpath(PAY_ORGANISER_XPATH)
            return
        
        waitList_button = self.find_element_by_xpath(WAITLIST_BUTTON_XPATH)
        if waitList_button:
            print("joining waitlist")
            waitList_button.click()
            sleep(5)

            self.click_elem_by_xpath(JOIN_WAITLIST_WITH_LOW_PRIO_XPATH)
            sleep(5)

            self.click_elem_by_xpath(PAY_ORGANISER_XPATH)
            return
        
        sleep(2)

    def find_element_by_xpath(self, xpath):
        print("finding elem for xpath: ", xpath)

        try:
            elem = self.browser.find_element(By.XPATH, xpath)
            return elem
        except:
            print("no elem found for xpath: ", xpath)
            return None
        

    def click_elem_by_xpath(self, xpath):
        button = self.find_element_by_xpath(xpath)
        if button:
            print("button found")

        button.click()

    #Check if Already RSVPed
    def __check_already_going(self):
        text = "You're going to this event!"
        print(self.browser.page_source)
        if text in self.browser.page_source:
            print("Already RSVP")
            return True
        else:
            return False


    def closeBrowser(self):
        self.browser.close()
        
    #Fetchs links of events from group name
    def fetch_events_by_group(self, group):

        group_link = f"https://www.meetup.com/{group}/events/"

        response = requests.get(group_link)

        if response.status_code != 200:
            print("Something Went Wrong! Please check Group Url")
            return []
        
        html_res = BeautifulSoup(response.text,"html.parser")

            # Grab the JSON-containing <script> block
        script_tag = html_res.find("script", {"id": "__NEXT_DATA__"})

        if script_tag:
            json_text = script_tag.string

            # Regex to find all eventUrl values
            event_urls = re.findall(r'"eventUrl"\s*:\s*"([^"]+)"', json_text)

            print("Extracted event URLs")

        else:
            print("No JSON script with id '__NEXT_DATA__' found!")

        return event_urls