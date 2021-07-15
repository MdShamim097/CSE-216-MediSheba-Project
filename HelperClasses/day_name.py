import datetime


class FindDayName:
    def __init__(self, entered_date):
        self.date = entered_date

    def find_day_name(self):
        day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = datetime.datetime.strptime(self.date, '%Y-%m-%d').weekday()
        return day_name[day]
