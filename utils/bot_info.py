import datetime as dt
from dateutil.relativedelta import relativedelta

class BotData:

    def __init__(self) -> None:
        self.birthday = dt.datetime(2022, 1, 4)
    
    def get_age(self) -> int:

        '''
            Get age of bot in years.
        '''

        current_time = dt.datetime.now()
        age = relativedelta(current_time, self.birthday).years

        return age
