import time as t

LOCAL_TIME = t.localtime()
DAY = LOCAL_TIME.tm_wday
HOUR = LOCAL_TIME.tm_hour
MIN = LOCAL_TIME.tm_min
LOCAL_DATA = open("data.py", "r")
SET_DATE = []
SET_DATE.append(LOCAL_DATA.readlines())
months = [" ", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
actualMonth = months[LOCAL_TIME.tm_mon]
days = ["monday", "thuesday", "wednessday", "thursday", "friday", "saturday", "sunday"]
print("===================================================================================")
print("Welcome!, the time is: ")
print(days[DAY] +" | "+ actualMonth +" "+ str(LOCAL_TIME.tm_mday) +" / "+ str(LOCAL_TIME.tm_year) +" | "+ str(HOUR), ':', str(MIN) + " hrs")

x = SET_DATE[0]
alarmON = x.pop(0)
alarmON = alarmON[:-1]
setHour = x.pop(0)
setHour = setHour[:-1]
setMin = x.pop(0)
setMin = setMin[:-1]

txt = ' '
for j in x:
    txt = txt + days[int(j)] + ' | '
    txt = txt
print("===================================================================================")
print("Alarm ON: ", alarmON)
print("Set on days: ", txt)
print("===================================================================================")


if HOUR == setHour and MIN == setMin:
    print("You must go to work")
else:
    pass

LOCAL_DATA.close()

def TIMER(SET_TIMER):
    """
    Set the working time
    :return:
    """

    list = []

    if (('pm' in SET_TIMER) or ('PM' in SET_TIMER)) and (':' in SET_TIMER):

        x = SET_TIMER.split(":")
        list.append(x[0])
        list.append(x[1][:-2])
        x = int(list[0])+12
        list[0]=str(x)

    elif (('am' in SET_TIMER) or ('AM' in SET_TIMER)) and (':' in SET_TIMER):
        x = SET_TIMER.split(":")
        list.append(x[0])
        list.append(x[1][:-2])
    return list


RESPONSE = input("Do you want to set an alarm to work?: ")

if (RESPONSE=='yes') or (RESPONSE=='YES') or(RESPONSE=='Yes') or (RESPONSE=='y') or (RESPONSE=='Y'):
    SET_TIMER = str(input("Enter the time you must working : "))
    TIMER = TIMER(SET_TIMER)
    SET_DATE = []
    print("Enter the days when you must working : ")

    for i in range(0, 7):
        x = days[i]
        y = input("Activate on " + str(x) + "?: ")
        if (y == 'yes') or (y == 'YES') or (y == 'Yes') or (y == 'y') or (y == 'Y'):
            SET_DATE.append(str(i))
        else:
            pass
    print("variable SET_TIMER: ", SET_TIMER)
    print("Variable TIMER:")
    print(TIMER)
    LOCAL_DATA = open("data.py", "w")
    LOCAL_DATA.write(SET_TIMER+'\n')
    LOCAL_DATA.write(str(TIMER[0])+'\n')
    LOCAL_DATA.write(str(TIMER[1])+'\n')
    for k in SET_DATE:
        LOCAL_DATA.write(k+'\n')
else:
    pass

LOCAL_DATA.close()

