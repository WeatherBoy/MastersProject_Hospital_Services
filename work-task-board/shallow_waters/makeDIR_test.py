import os
import datetime

path = "results/"
if os.path.exists(path + "2024_Week_38"):
    print("Path already exists")
else:
    os.makedirs(path + "2024_Week_38")


def get_week_dates_from_today(today):
    # Get the ISO calendar details for today (year, week number, and weekday)
    year, week, weekday = today.isocalendar()

    # Find the start of the week (Monday)
    start_of_week = today - datetime.timedelta(days=weekday - 1)

    # Generate all dates in the week
    return [start_of_week + datetime.timedelta(days=i) for i in range(7)]


today = datetime.date.today()
week_dates = get_week_dates_from_today(today)
print(type(week_dates[0]))
for week_date in week_dates:
    print(week_date)

print()
for week_date in week_dates:
    print(str(week_date))
