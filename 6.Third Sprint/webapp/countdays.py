from datetime import date, timedelta
from datetime import datetime

def get_start_to_end(start_date, end_date):
    date_list = []
    print(start_date, end_date)
    for i in range(0, (end_date - start_date).days + 1):
        date_list.append(  str(start_date + timedelta(days=i))  ) #<-- here
    return date_list


def main(d1, d2):
    date_str1 = d1
    date_str2 = d2
    print(date_str1, date_str2)

    sd = datetime.strptime(date_str1, '%Y-%m-%d').date()
    ed = datetime.strptime(date_str2, '%Y-%m-%d').date()

    dates = get_start_to_end(sd, ed)
    return dates



if __name__ == '__main__':
        
    date_str1 = '2023-04-13'
    date_str2 = '2023-04-13'

    sd = datetime.strptime(date_str1, '%Y-%m-%d').date()
    ed = datetime.strptime(date_str2, '%Y-%m-%d').date()

    dates = get_start_to_end(sd, ed)
    print(dates)

    