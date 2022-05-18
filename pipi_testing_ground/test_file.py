import time

#current date

#current time

#date of reservation

# start time of reservation

#end time of reservation


import datetime


#format_string = "%Y-%m-%dT%H:%M:%S.%f"
#date_string = "2015-11-31T13:45:00.000"
#datetime.datetime.strptime(date_string, format_string)
'''
#date_now = datetime.date.today()
time_now = datetime.datetime.now()
#print (date_now)
print (time_now)

date = datetime.datetime.strptime(time_now, "%Y %M %D  %H:%M:%S.%f")

print (date)
'''
'''
import datetime

# datetime object containing current date and time
now = datetime.datetime.now()
 
print("now =", now)

# dd/mm/YY H:M:S
#dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
date_now = now.strftime("%d-%m-%Y")
time_now = now.strftime("%H-%M-%S")
print("date =", date_now)
print("time =", time_now)	

'''

import datetime

first_date = datetime.datetime.today()
second_date = datetime.date(2015, 12, 16)

result = first_date - second_date
print(result)