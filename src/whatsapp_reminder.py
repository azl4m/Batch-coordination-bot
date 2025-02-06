import gspread
import pywhatkit as kit
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time
import random

# Step 1: Google Sheets API Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("./whatsapp-reminder-bot-03d3534c6d33.json", scope)
client = gspread.authorize(creds)
# List of motivational messages
motivational_messages = [
    "Hey {name}, did you know? People who complete tasks on time are 99% more awesome! 😎 Submit your audio task now!",
    "Hi {name}, don't let procrastination win today! 🚀 Get your task done before 10 PM and flex on the rest!",
    "Hey {name}, submitting your task = instant productivity boost! 🚀 Let’s make it happen before 10 PM!",
    "Hello {name}, imagine how relaxed you'll feel once it's done! ☕ Finish your audio task now and enjoy the rest of your day!",
    "Hey {name}, challenge yourself! Can you submit your task before 10 PM? I bet you can! 💪",
    "Hi {name}, let's turn your ‘I’ll do it later’ into ‘I just did it!’ ✅ Submit your audio now!",
    "Hey {name}, what if I told you submitting your task now gives you an extra boost of happiness? 😆 Try it and see!",
    "Hi {name}, your future self will thank you for doing it now! 🎙️ Let’s get this task done!",
    "Hello {name}, you’ve got the talent—now show the discipline! 💯 Submit your task and own the day!",
    "Hey {name}, the sooner you finish, the sooner you can relax! ☀️ Submit your task before 10 PM and enjoy!",
    "Hello {name}, perfection isn't required—progress is! 🎙️ Give it your best shot and submit your task before 10 PM!",
    "Hi {name}, winners don’t wait for deadlines—they beat them! 🏁 Submit your audio task now and stay ahead!"
]
# Step 2: Open your Google Sheet
spreadsheet = client.open("Audio task submission")  # Change to your sheet name
sheet = spreadsheet.sheet1  # Use the first sheet

# Step 3: Read Data
data = sheet.get_all_records()

# # Step 4: Get Pending Users
# pending_users = [row for row in data if row["Status"] != "YES"]

# # Step 5: WhatsApp Message
# message = "Reminder: You haven't submitted today's audio task. Please submit before 10 PM."

# # Get current time
# now = datetime.now()
# hour, minute = now.hour, now.minute + 1  # Sends in the next minute


# for user in pending_users:
#     phone = user["WhatsApp Number"]
#     kit.sendwhatmsg_instantly(phone, message, wait_time=10, tab_close=True)
#     print(f"Reminder sent to {user['Name']}")
for row in data:
    name = row["Name"]
    phone = row["WhatsApp Number"]
    submitted = row["Status"]

    if submitted.lower() == "no":  # Send reminder only if they haven't submitted
        # Select a random motivational message
        message = random.choice(motivational_messages).format(name=name)
        
        try:
            # Attempt to send WhatsApp message
            kit.sendwhatmsg_instantly(phone, message, wait_time=10, tab_close=True)
            print(f"Reminder sent successfully to {name}!")
            time.sleep(2)  # Delay between messages to prevent overload
        except Exception as e:
            print(f"Failed to send reminder to {name}. Error: {e}")
            
print("Reminder process completed!")
#py whatsapp_reminder.py