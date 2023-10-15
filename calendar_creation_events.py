import datetime

def create_calendar_events(start_date, end_date, shift_duration, participant_names, time_window_start=None, time_window_end=None, time_window_days=[0,1,2,3,4,5,6]):
    next_participant = 0
    calendar_events = []
    
    shift_start = start_date
    shift_end = shift_start + shift_duration

    while shift_start < end_date:

        person = participant_names[next_participant]

        shift_start_actual = shift_start
        shift_end_actual = shift_end

        if time_window_start is not None and time_window_end is not None:
            sub_shift_start = shift_start_actual
            sub_shift_start = sub_shift_start.replace(hour=time_window_start.hour, minute=time_window_start.minute, second=time_window_start.second)
            sub_shift_end = shift_start_actual
            sub_shift_end = sub_shift_end.replace(hour=time_window_end.hour, minute=time_window_end.minute, second=time_window_end.second)
            
            while sub_shift_start < shift_end_actual:
                if time_window_days is not None:
                    if sub_shift_start.weekday() not in time_window_days:
                        sub_shift_start += datetime.timedelta(days=1)
                        sub_shift_end += datetime.timedelta(days=1)
                        continue

                calendar_events.append({
                    "title": "Shift (" + person + ")",
                    "start": sub_shift_start.isoformat(),
                    "end": sub_shift_end.isoformat(),
                    "resourceId": 'participant_'+str(next_participant),
                })

                sub_shift_start += datetime.timedelta(days=1)
                sub_shift_end += datetime.timedelta(days=1)
        else:
            if time_window_days is not None:
                if shift_start_actual.weekday() not in time_window_days:
                    shift_start = shift_end
                    shift_end = shift_start + shift_duration
                    continue

            calendar_events.append({
                "title": "Shift (" + person + ")",
                "start": shift_start_actual.isoformat(),
                "end": shift_end_actual.isoformat(),
                "resourceId": 'participant_'+str(next_participant),
            })

        next_participant += 1
        if next_participant >= len(participant_names):
            next_participant = 0

        shift_start = shift_end
        shift_end = shift_start + shift_duration
    
    return calendar_events