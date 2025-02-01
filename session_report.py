import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import pytz
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")

# -------------------------------
# Step 1: Set up Google Sheets API
# -------------------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
client = gspread.authorize(creds)

# -------------------------------
# Step 2: Open your Google Sheet
# -------------------------------
sheet = client.open("Audio task submission").sheet1  

# -------------------------------
# Step 3: Fetch data from the sheet
# -------------------------------
data = sheet.get_all_records()

attendees = [row["Name"] for row in data if row["Status"].strip().lower() == "yes"]
absentees = [row["Name"] for row in data if row["Status"].strip().lower() == "no"]

# -------------------------------
# Step 4: Set up header details with the correct date
# -------------------------------
batch = "BCR61- Combined"
# Using a specific timezone to ensure the correct date
tz = pytz.timezone("Asia/Kolkata")  # Change to your timezone if needed
report_date = datetime.datetime.now(tz).strftime("%d-%m-%Y")
time_slot = "11:30 AM - 12:30 PM"
trainers = "Rohan N Devasia, Herrick Joseph"
coordinators = "Nishad & Lithiya Thomas"
topic_line = "Topic - [Details to be added later]"
tldv_link = "https://tldv.io/app/meetings/679b17081309660013f4f37d/"
prepared_by = "Nishad"

# -------------------------------
# Step 5: Construct the report message
# -------------------------------
report_message = f"""
🖥 Batch: {batch}
🗓 Date: {report_date}
⏱ Time: {time_slot}

👩‍💻 Trainer: {trainers}
👨🏻‍💼 Coordinator: {coordinators}

✨ {topic_line}

✅ Attendees:
{chr(10).join([f"{i+1}. {name}" for i, name in enumerate(attendees)])}

🚫 Absentees:
{chr(10).join([f"{i+1}. {name}" for i, name in enumerate(absentees)])}

🎥 tldv Link:
{tldv_link}

📋 Prepared by:
{prepared_by}
"""

# -------------------------------
# Step 6: Save the report to a text file
# -------------------------------
output_file = "session_report.txt"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(report_message)

print(f"✅ Report generated and saved to {output_file}")
