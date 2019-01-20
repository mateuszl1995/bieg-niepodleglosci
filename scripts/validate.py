import pandas
import re
import datetime as dt
import numpy as np
import math

time_pattern = re.compile('0[0-5]:[0-5][0-9]:[0-5][0-9].*')
category_pattern = re.compile('^[MK](16|[0-9]0\+?)$')
year = dt.datetime.now().year

def load_and_process(path):
    df = pandas.read_csv(path, ';')
    if df.columns[0] == 'Unnamed: 0':
        df.drop(['Unnamed: 0'], axis=1, inplace=True)
    df['half-time'] = 0
    df['time'] = 0
    df['brutto-time'] = 0
    return df.to_records(index=False)

def time2sec(str_time, default_value):
    if time_pattern.search(str_time) == None:
        return default_value
    pt =dt.datetime.strptime(str_time[0:8],'%H:%M:%S')
    return pt.second+pt.minute*60+pt.hour*3600

def validate(data):
    correct = True
    for i in range(len(data)):
        row = data[i]
        if (
                row['birth-year'] < 1900 or row['birth-year'] > year
                or category_pattern.search(row['category']) == None
                or row['place-W'] * row['place-M'] > 0
                or (row['place-W'] == -1 and row['category'][0] == 'K')
                or (str(row['s-time']) != 'nan' and time_pattern.search(row['s-time']) == None)
                or time_pattern.search(row['s-brutto-time']) == None
                or (str(row['s-half-time']) != 'nan' and time_pattern.search(row['s-half-time']) == None)):
            print(row)
            correct = False
        else:
            row['time'] = time2sec(row['s-time'], 0)
            row['brutto-time'] = time2sec(row['s-brutto-time'], row['time'])
            try:
                row['half-time'] = time2sec(row['s-half-time'], row['time'] / 2)
            except:
                row['half-time'] = row['time'] / 2
    if correct:
        print('Walidacja danych przebiegła pomyślnie. Nie znaleziono błędów.')
        
paths = ['./data/bieg-2016.csv', './data/bieg-2017.csv', './data/bieg-2018.csv']
for path in paths:
    print('Wczytywanie i przetwarzanie pliku ' + path)
    data = load_and_process(path)
    print('Walidacja pliku ' + path)
    validate(data)
    print('-----------------------------')
    df = pandas.DataFrame(data)
    df.to_csv(path, ';', index=False)