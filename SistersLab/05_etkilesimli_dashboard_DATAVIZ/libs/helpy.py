import pandas as pd

class BUTTON:
    def __init__(self, click):
        self.click = click

    def isNew(self, newClick):
        if (self.click == newClick):
            return False
        elif ((newClick == 0) | (newClick == None)):
            return False
        else:
            self.click = newClick
            return True

def time_filter(df, start_date_, end_date_):
    return df[(df['PLAY_DATE'] > pd.to_datetime(start_date_)) & (df['PLAY_DATE'] < pd.to_datetime(end_date_))]