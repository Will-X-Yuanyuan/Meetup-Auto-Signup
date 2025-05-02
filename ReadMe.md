# 📅 Auto RSVP for Meetup.com

This program will automatically RSVP to Meetup.com events at a scheduled time.

Note that the program will STOP running if your PC goes to sleep! So make sure your PC is open when the program is running!

Also, if you have the program running at home, it is best to avoid signing in to Meetup right before the scheduled RSVP time at other places (The system may flag it as suspicious login if you login at completely different places at around the same time)


## 📜 Requirements
1. Have python installed
2. Have Google Chrome installed
3. Have an account for Meetup.com

## 🔧 Setup Instructions

### 1. Clone the repository
```
git clone https://github.com/Will-X-Yuanyuan/Meetup-Auto-Signup.git 
cd AutoRSVP
```

### 2. Install required Python packages

```
pip3 install -r requirements.txt
```

### 3. Setup your configuration
- Create your own `config.yaml`:
- Edit `config.yaml` and fill in the details:

  - Email
  - Password
  - Events list (link and RSVP time)
- See `config.example.yaml` for an example

Note:
The RSVP time format must be HH:MM-DD-MM-YYYY.

### 4. Run the script
```
python main.py
```
