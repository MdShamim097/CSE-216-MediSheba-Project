import datetime
'''
start = datetime.datetime.strptime("2021-01-01", "%Y-%m-%d")
end = datetime.datetime.strptime("2021-01-25", "%Y-%m-%d")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]

for date in date_generated:
    print(date.strftime("%Y-%m-%d"))

'''


class FindSequenceOfDays:
    def __init__(self, start_day, end_day):
        self.enter_day = start_day
        self.exit_day = end_day

    def generate_sequence(self):
        start = datetime.datetime.strptime(self.enter_day, "%Y-%m-%d")
        end = datetime.datetime.strptime(self.exit_day, "%Y-%m-%d")
        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]
        return date_generated
