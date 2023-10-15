import datetime
import streamlit as st
from streamlit_calendar import calendar
from colorsys import hsv_to_rgb

from calendar_creation_events import create_calendar_events

def get_hex_color_list(num_colors=5, saturation=1.0, value=1.0):
    hex_colors = []
    hsv_colors = [[float(x / num_colors), saturation, value] for x in range(num_colors)]
    
    for hsv in hsv_colors:
       hsv = [int(x * 255) for x in hsv_to_rgb(*hsv)]
    
       # Formatted as hexadecimal string using the ':02x' format specifier
       hex_colors.append(f"#{hsv[0]:02x}{hsv[1]:02x}{hsv[2]:02x}")
    
    return hex_colors

now = datetime.datetime.now()

sd_cols = st.columns(2)
sd = sd_cols[0].date_input("Rota start Date", now)
start_time = sd_cols[1].time_input("Start Time", now)

ed_cols = st.columns(2)
ed = ed_cols[0].date_input("Rota end Date", now+datetime.timedelta(days=30))
end_time = ed_cols[1].time_input("End Time", value=now)

duration_cols = st.columns(2)
shift_duration_value = duration_cols[0].number_input("Shift Duration", value=7)
shift_duration_unit = duration_cols[1].selectbox("Shift Duration Unit", ['Days','Hours'])

shift_duration = datetime.timedelta()
if shift_duration_unit == 'Days':
    shift_duration = datetime.timedelta(days=shift_duration_value)
else:
    shift_duration = datetime.timedelta(hours=shift_duration_value)


if 'participants' not in st.session_state:
    st.session_state['participants'] = 2

if st.button("+Add"):
    st.session_state['participants'] += 1

for i in range(st.session_state['participants']):
    st.session_state['participant_'+str(i)] = st.text_input("Participant Name", key=i, value='Participant '+str(i+1))

time_window_on = st.toggle('Limit shift to specific times')

if time_window_on:
    tw_cols = st.columns(2)
    time_window_start = tw_cols[0].time_input("Time Window Start", datetime.time(hour=9))
    time_window_end =   tw_cols[1].time_input("Window End", datetime.time(hour=17))
    time_window_days_option = st.selectbox("Shift days", ['Every day','Weekdays', 'Weekends', 'Custom'])
    
    if time_window_days_option == 'Custom':
        time_window_days_select = st.multiselect("Select days", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

participant_names = []

for i in range(st.session_state['participants']):
    participant_names.append(st.session_state['participant_'+str(i)])

resources = []
color_list = get_hex_color_list(num_colors=st.session_state['participants'], saturation=1, value=0.75)
for i in range(st.session_state['participants']):
    resources.append({
        "id": 'participant_'+str(i), 
        "participant": participant_names[i], 
        "title": participant_names[i],
        "eventColor": color_list[i],
    })

days_enabled = None
if time_window_on:
    if time_window_days_option != 'Custom':
        days_enabled = [0,1,2,3,4] if  time_window_days_option == 'Weekdays' else [5,6] if time_window_days_option == 'Weekends' else None
    else:
        days_enabled = []
        if 'Monday' in time_window_days_select:
            days_enabled.append(0)
        if 'Tuesday' in time_window_days_select:
            days_enabled.append(1)
        if 'Wednesday' in time_window_days_select:
            days_enabled.append(2)
        if 'Thursday' in time_window_days_select:
            days_enabled.append(3)
        if 'Friday' in time_window_days_select:
            days_enabled.append(4)
        if 'Saturday' in time_window_days_select:
            days_enabled.append(5)
        if 'Sunday' in time_window_days_select:
            days_enabled.append(6)


calendar_events = create_calendar_events(
    datetime.datetime.combine(sd, start_time), 
    datetime.datetime.combine(ed, end_time), 
    shift_duration, 
    participant_names,
    time_window_start=time_window_start if time_window_on else None,
    time_window_end=time_window_end if time_window_on else None,
    time_window_days=days_enabled
    )

calendar_options = {
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "",
    },
    "initialView": "timeGridWeek",
    "initialDate": sd.isoformat(),
    "slotDuration": "1:00:00",
    "resourceGroupField": "participant",
    "resources": resources,
}
    
custom_css="""
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 2rem;
        }
    """,

text_contents = '''Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private'''
for event in calendar_events:
    text_contents += '\n'
    text_contents += event['title'] + ','
    text_contents += event['start'].split('T')[0] + ','
    text_contents += event['start'].split('T')[1] + ','
    text_contents += event['end'].split('T')[0] + ','
    text_contents += event['end'].split('T')[1] + ','
    text_contents += 'False,'
    text_contents += ','
    text_contents += ','
    text_contents += 'False'

st.download_button('Download CSV', text_contents, file_name='rota.csv', mime='text/csv')

calendar = calendar(events=calendar_events, options=calendar_options, custom_css=custom_css)
st.write(calendar)