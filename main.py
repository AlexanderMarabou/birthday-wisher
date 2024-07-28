import smtplib
import datetime as dt
import pandas as pd
import random

MY_EMAIL = "alexander.marabu@gmail.com"
PASSWORD = ""

# Gets the current time and sets the send time
now = dt.datetime.now()
current_month = now.month
current_day = now.day
current_hour = now.hour
current_minute = now.minute
current_time = dt.time(current_hour, current_minute)
send_time = dt.time(8, 30)

# Runs the script at the scheduled send time
if current_time == send_time:
    # Checks if today is someone's birthday
    birthdays = pd.read_csv("birthdays.csv")
    birthdays_found = birthdays[(birthdays['month'] == current_month) & (birthdays['day'] == current_day)]
    if not birthdays_found.empty:
        # Fetches birthday person's name and email
        for index, row in birthdays_found.iterrows():
            birthday_name = row['name']
            birthday_email = row['email']
            # Selects a random letter template and replaces [NAME] from the letter
            with open(f"letter_templates/letter_{random.randint(1, 3)}.txt") as letter:
                raw_letter = letter.read()
                letter_with_name = raw_letter.replace("[NAME]", f"{birthday_name}")
            # Sends the email to the birthday person with personalized subject
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL, to_addrs=birthday_email,
                                    msg=f"Subject: Happy birthday courtesy of Python :) {birthday_name}"
                                        f"\n\n{letter_with_name}")
