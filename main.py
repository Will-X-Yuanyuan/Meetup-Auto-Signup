from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from time import sleep

class Autorsvp():
	def __init__(self,email,password):
	
		self.browser = webdriver.Chrome()
		self.browser.get("https://www.meetup.com")

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

		sleep(1)

		print("successfully logged in")



	def rsvp_meeting(self,link):
		self.browser.get(link)
		sleep(2)


		#If Already RSVP'ed

		# if self.__check_already_going():
		# 	return

		#Click RSVP Button

		if self.browser:
			print("got browser")
		
		try:
			attend_button = self.browser.find_element(By.XPATH, ("//*[@data-testid='attend-irl-btn']"))
		except:
			print("no attend button")
		
		if not attend_button:
			try:
				attend_button = self.browser.find_element(By.XPATH, ("//*[@data-testid='waitlist-btn']"))
			except:
				print("no waitlist button")
		
		if attend_button:
			print("clicking attend")
			attend_button.click()
			self.pay_organiser()

		sleep(5)

	def pay_organiser(self):
		sleep(2)
		button = self.browser.find_element(By.XPATH, ("/html/body/div[1]/div[3]/div/div[1]/div/div/div/div/div[2]/div[3]/button"))
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
def fetch_events_by_group(group):

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



if __name__ == "__main__":


	print("\n================ Auto RSVP Meetup.com ================\n")
	
	email = input("Enter your email: ")
	password = input("Enter your password: ")
	groups = []

	no_groups = int(input("\nEnter the number(count) of groups you want to AutoRSVP: "))
	
	print("\nEnter the groups name in each line\n")

	for i in range(no_groups):
		usrinpt =  input("Enter group -> ")
		groups.append(usrinpt)


	print("\n ====== Auto RSVPing (Meetup.com) =======")

	waitTime = 60  #60 Minutes


	#Storing Visited Links to Increase Performance
	visitedLinks = set()

	while True:
		# Run this every 1 hour
		
		# Setup Browser
		rsvper = Autorsvp(email,password)


		# Login
		rsvper.login_with_email()

		# Get Groups Details

		for grp in groups:
				
			print(grp)

			eventLinks = fetch_events_by_group(grp)

			for link in eventLinks:
				print(link)

				if link in visitedLinks:
					continue

				if link != "https://www.meetup.com/melbourne-volleyball-academy/events/307133912/":
					continue

				visitedLinks.add(link)

				rsvper.rsvp_meeting(link)

				sleep(6)
			
			print("checked all event links")

		# rsvper.closeBrowser()
		sleep(waitTime*60)

