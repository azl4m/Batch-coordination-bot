import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# 🔹 Step 1: Setup Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("./whatsapp-reminder-bot-16ca6d99dbf2.json", scope)
client = gspread.authorize(creds)

# 🔹 Step 2: Open the Google Sheet
sheet = client.open("Audio task submission").sheet1  # Replace with your actual Google Sheet name

# 🔹 Step 3: Fetch all data
data = sheet.get_all_records()

# 🔹 Step 4: Get today's date
today_date = datetime.datetime.today().strftime("%d-%m-%Y")

# 🔹 Step 5: Separate submitted and not submitted
submitted_list = [row["Name"] for row in data if row["Status"].lower() == "yes"]
not_submitted_list = [row["Name"] for row in data if row["Status"].lower() == "no"]

# 🔹 Step 6: Format the report
report_message = f"""
🔰 AUDIO TASK REPORT 🔰

✨ Batch: BCR-61
📅 Date: {today_date}

✅ Submitted ({len(submitted_list)}):
{chr(10).join([f"{i+1}. {name}" for i, name in enumerate(submitted_list)])}

❌ Not Submitted ({len(not_submitted_list)}):
{chr(10).join([f"{i+1}. {name}" for i, name in enumerate(not_submitted_list)])}

📄 Report Prepared By:

Nabeel
Nidhin
"""

# 🔹 Step 7: Save the report message to a text file with UTF-8 encoding
file_path = "audio_task_report.txt"
with open(file_path, "w", encoding="utf-8") as file:
    file.write(report_message)

print(f"✅ Report saved successfully to {file_path}")
