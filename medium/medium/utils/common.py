
from datetime import datetime

month_dict = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}


def date_convert(value):

    month = month_dict[value[:3]]
    if len(value) > 6:
        year = int(value[-4:])
        day = int(value[4:-5])
    else:
        year = datetime.now().year
        day = int(value[4:])

    date = datetime(year, month, day)
    return date


def claps_convert(value):

    if value[-1] == 'K':
        return int(float(value[:-2])*1000)
    return int(value)


if __name__ == '__main__':
    print(date_convert('Jan 1'))
    print(claps_convert('2.7K'))
