import time
import sched
from autoRsvp import Autorsvp
from time import sleep
from datetime import datetime

import yaml
import os
import shutil

BUFFER_SECONDS = 2
EARLY_LOGIN_SECONDS = 40

def execute(email, password, rsvp_time, event_link):
    print(f"[{datetime.now()}] Starting login process...")

    rsvper = Autorsvp(email, password)
    rsvper.login_with_email()

    start_time = rsvp_time + BUFFER_SECONDS
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enterabs(start_time, 1, rsvp, argument=(rsvper, event_link))

    print(f"[{datetime.now()}] Scheduled RSVP at local time {datetime.fromtimestamp(start_time)}. Waiting...")
    scheduler.run()

    rsvper.closeBrowser()
    print(f"[{datetime.now()}] Browser closed. Done.")

def rsvp(rsvper, event_link):
    print(f"[{datetime.now()}] Executing RSVP for event: {event_link}")
    
    start_time = time.time()

    rsvper.rsvp_meeting(event_link)

    elapsed_time = time.time() - start_time
    print(f"[{datetime.now()}] RSVP completed in {elapsed_time:.2f} seconds.")

def load_config():
    config_file = 'config.yaml'

    if not os.path.exists(config_file):
        print("Copying default config.example.yaml... Make sure you configure config.yaml!")
        shutil.copy('config.example.yaml', 'config.yaml')
        exit(1)

    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    print("\n================ Auto RSVP Meetup.com ================\n")
    config = load_config()

    # Extract email and password
    email = config["email"]
    password = config["password"]

    # Extract events
    events = [(event["link"], event["rsvp_time"]) for event in config["events"]]

    print(f"Loaded {len(events)} events from config file.")

    print("\n======= Setup scheduler to Auto RSVP (Meetup.com) =======")

    scheduler = sched.scheduler(time.time, time.sleep) 
    for eventLink, rsvp_time in events:
        try:
            dt = datetime.strptime(rsvp_time, "%H:%M-%d-%m-%Y")
        except:
            print("time input in the wrong format. Defaulting to current time")
            dt = datetime.now()

        # Convert to epoch (Unix timestamp)
        epoch_time = int(dt.timestamp())
        print(f"[{datetime.now()}] Created schedule for local time: ({dt})")
        
        scheduler.enterabs(epoch_time - EARLY_LOGIN_SECONDS, 1, execute, argument= (email, password, epoch_time, eventLink))
    
    scheduler.run() 

