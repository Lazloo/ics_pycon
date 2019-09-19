from icalendar import Calendar, Event
import pandas as pd
import json
import urllib.request

# Load Json
url_link = "https://raw.githubusercontent.com/PYCONDE/www/master/website/databags/schedule_databag.json"
with urllib.request.urlopen(url_link) as url:
    data = json.loads(url.read().decode())
# with open('https://github.com/PYCONDE/www/tree/master/website/databags/schedule_databag.json') as f:
#     d = json.load(f)
#     print(d)

# Collect important information
collect_date_event = []
for i_dates in data.get('dates'):
    for i_room in i_dates['rooms']:
        for i_session in i_room['sessions']:
            if (len(i_session['title']) > 0) & (i_session['type'] != "sessionname"):
                collect_date_event.append((

                    i_session['title'],
                    i_dates['datum'],
                    i_session['time'],
                    i_session['duration'].split(':'),
                    i_room['room_name'],
                ))

# Initialize Calender
cal = Calendar()
cal.add('prodid', 'PyCon Berlin 2019')
cal.add('version', '1.0')

# Fill Calender
for i in range(len(collect_date_event)):
    start_time = pd.Timestamp(collect_date_event[i][1] + ' ' + collect_date_event[i][2])
    if collect_date_event[i][3][0] == '':
        end_time = start_time + pd.Timedelta(1, unit='min')
    else:
        end_time = (start_time +
                    pd.Timedelta(int(collect_date_event[i][3][0]), unit='h') +
                    pd.Timedelta(int(collect_date_event[i][3][1]),
                                 unit='min'))  # min only exists for pandas 0.25 upwards
    event = Event()
    event.add('summary', collect_date_event[i][0])
    event.add('dtstart', start_time)
    event.add('dtend', end_time)
    event.add('location', collect_date_event[i][4])
    cal.add_component(event)

# Save Calender
f = open('pycon_de_2019.ics', 'wb')
f.write(cal.to_ical())
f.close()
