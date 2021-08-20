import numpy as np
import pandas as pd

def preprocess(df):
    df['Weight'] *= 0.453592 # ibs to kg
    df['Height'] *= 2.54 # inch to cm

    df['bmi'] = df['Weight'] / ((df['Height']/100)**2) # bmi hesabi
    df = np.round(df,2) # kusurat basamaklari yuvarlama
    df = df[df['bmi'] < 100] # Hatali bmi degerini dusmek icin
    df['counts'] = 1

    def bmi_sonuc(skor):
        if (skor < 18.5):
            return 'Zayif'
        elif (skor < 24.99):
            return 'Normal'
        elif (skor < 29.99):
            return 'Fazla Kilolu'
        elif (skor < 39.99):
            return 'Obez'
        else:
            return 'Morbid Obez'

    df['bmi_sonuc'] = df['bmi'].apply(lambda x: bmi_sonuc(x))
    return df