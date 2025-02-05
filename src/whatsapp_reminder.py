import gspread
import pywhatkit as kit
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time

# Step 1: Google Sheets API Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("./whatsapp-reminder-bot-03d3534c6d33.json", scope)
client = gspread.authorize(creds)

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
        message = f"Hi {name}, this is a reminder to submit your audio task before 10 PM. Please do it soon!"
        
        try:
            # Attempt to send WhatsApp message
            kit.sendwhatmsg_instantly(phone, message, wait_time=10, tab_close=True)
            print(f"Reminder sent successfully to {name}!")
            time.sleep(1)
        except Exception as e:
            print(f"Failed to send reminder to {name}. Error: {e}")
            
print("Reminder process completed!")
#py whatsapp_reminder.py