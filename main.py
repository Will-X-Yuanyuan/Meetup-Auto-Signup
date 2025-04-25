import time
import sched
from autoRsvp import Autorsvp
from time import sleep
from datetime import datetime

def execute(email, password, eventLink):
	print(f"executing at time {datetime.now()} for event {eventLink}")

	rsvper = Autorsvp(email,password)
	rsvper.login_with_email()

	rsvper.rsvp_meeting(eventLink)

	rsvper.closeBrowser()
	return

if __name__ == "__main__":


	print("\n================ Auto RSVP Meetup.com ================\n")
	
	email = input("Enter your email: ")
	password = input("Enter your password: ")
	
	# groups = []
	# no_groups = int(input("\nEnter the number(count) of groups you want to AutoRSVP: "))
	
	# print("\nEnter the groups name in each line\n")

	# for i in range(no_groups):
	# 	usrinpt =  input("Enter group -> ")
	# 	groups.append(usrinpt)

	events = []
	no_events = int(input("\nEnter the number(count) of events you want to AutoRSVP: "))
	
	print("\nEnter the event link and time of RSVP in each line\n")

	for i in range(no_events):
		usrinptEventLink =  input("Enter event link -> ")
		usrinptRsvpTime = input("Enter the time to RSVP for the above event in the format (HH:MM-DD-MM-YYYY): ")
		eventAndTime = [usrinptEventLink, usrinptRsvpTime]
		events.append(eventAndTime)


	print("\n ====== Setup scheduler to Auto RSVP (Meetup.com) =======")

	scheduler = sched.scheduler(time.time, time.sleep) 
	for eventAndTime in events:
		dt = datetime.strptime(eventAndTime[1], "%H:%M-%d-%m-%Y")

		# Convert to epoch (Unix timestamp)
		epoch_time = int(dt.timestamp())
		print(f"created schedule at local time ({dt}) and epoch time: ({epoch_time})")

		scheduler.enterabs(epoch_time, 1, execute, argument= (email, password, eventAndTime[0]))
	
	scheduler.run() 
	# waitTime = 60  #60 Minutes


	#Storing Visited Links to Increase Performance
	# visitedLinks = set()

	# while True:
	# 	# Setup Browser
	# 	rsvper = Autorsvp(email,password)


	# 	# Login
	# 	rsvper.login_with_email()

	# 	for eventAndTime in events:
	# 		rsvper.rsvp_meeting(eventAndTime[0])
	# 		sleep(5)

		# # Get Groups Details
		# for grp in groups:
				
		# 	print(grp)

		# 	eventLinks = rsvper.fetch_events_by_group(grp)

		# 	for link in eventLinks:
		# 		print(link)

		# 		if link in visitedLinks:
		# 			continue

		# 		if link != "https://www.meetup.com/melbourne-volleyball-academy/events/307133912/":
		# 			continue

		# 		visitedLinks.add(link)

		# 		rsvper.rsvp_meeting(link)

		# 		sleep(6)
			
		# 	print("checked all event links")



		# rsvper.closeBrowser()
		# sleep(waitTime*60)

