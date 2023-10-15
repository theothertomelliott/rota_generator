import unittest

import datetime
from calendar_creation_events import create_calendar_events

class TestCreateEvents(unittest.TestCase):
    def test_create_events(self):
        events = create_calendar_events(
            start_date=datetime.datetime(2021, 1, 1, 9, 0, 0),
            end_date=datetime.datetime(2021, 1, 1, 17, 0, 0),
            shift_duration=datetime.timedelta(hours=5),
            participant_names=['John', 'Jane']
        )
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]['title'], 'Shift (John)')
        self.assertEqual(events[1]['title'], 'Shift (Jane)')

    def test_single_time_window(self):
        events = create_calendar_events(
            start_date=datetime.datetime(2021, 1, 1, 6, 0, 0),
            end_date=datetime.datetime(2021, 1, 5, 6, 0, 0),
            shift_duration=datetime.timedelta(hours=24),
            participant_names=['John', 'Jane'],
            time_window_start=datetime.time(hour=9),
            time_window_end=datetime.time(hour=17),
        )
        self.assertEqual(len(events), 4)
        self.assertEqual(events[0]['start'], '2021-01-01T09:00:00')
        self.assertEqual(events[0]['end'], '2021-01-01T17:00:00')
    
    def test_single_time_window_days(self):
        events = create_calendar_events(
            start_date=datetime.datetime(2023, 10, 14, 9, 0, 0),
            end_date=datetime.datetime(2023, 10, 17, 10, 0, 0),
            shift_duration=datetime.timedelta(hours=24),
            participant_names=['John', 'Jane'],
            time_window_days=[0,1,2,3,4]
        )

        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]['title'], 'Shift (John)')
        self.assertEqual(events[1]['title'], 'Shift (Jane)')
        self.assertEqual(events[0]['start'], '2023-10-16T09:00:00')
        self.assertEqual(events[0]['end'], '2023-10-17T09:00:00')

    def test_single_business_hours_shifts(self):
        events = create_calendar_events(
            start_date=datetime.datetime(2023, 10, 14, 9, 0, 0),
            end_date=datetime.datetime(2023, 11, 16, 10, 0, 0),
            shift_duration=datetime.timedelta(hours=7*24),
            participant_names=['John', 'Jane'],
            time_window_start=datetime.time(hour=9),
            time_window_end=datetime.time(hour=17),
            time_window_days=[0,1,2,3,4]
        )

        self.assertEqual(events[0]['title'], 'Shift (John)')
        self.assertEqual(events[0]['start'], '2023-10-16T09:00:00')
        self.assertEqual(events[0]['end'], '2023-10-16T17:00:00')
        self.assertEqual(events[1]['start'], '2023-10-17T09:00:00')
        self.assertEqual(events[1]['end'], '2023-10-17T17:00:00')
        self.assertEqual(events[1]['title'], 'Shift (John)')

if __name__ == '__main__':
    unittest.main()