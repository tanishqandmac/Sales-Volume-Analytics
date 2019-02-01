from datetime import datetime as dt
from dateutil import tz
import datetime

begninning = " 00:00:00{}"
ending = " 23:59:59{}"

def datePicker(date, offset):
    if (date=="today"):
        date = thisDay(offset)
    elif (date=="yesterday"):
        date = yesterday(offset)
    elif (date=="week"):
        date = thisWeek(offset)
    elif (date=="month"):
        date = thisMonth(offset)
    elif (date=="year"):
        date = thisYear(offset)
    elif (date=="lastweek"):
        date = lastWeek(offset)
    elif (date=="lastmonth"):
        date = lastMonth(offset)
    elif (date=="1stquarter"):
        date = firstQuarter(offset)
    elif (date=="2ndquarter"):
        date = secondQuarter(offset)
    elif (date=="3rdquarter"):
        date = thirdQuarter(offset)
    elif (date=="4thquarter"):
        date = fourthQuarter(offset)
    else:
        try:
            customdate = date.split("-")
            date = [datetime.datetime.strptime(customdate[0], "%m/%d/%Y").strftime("%Y-%m-%d")+str(begninning.format(offset)),
                    datetime.datetime.strptime(customdate[1], "%m/%d/%Y").strftime("%Y-%m-%d")+str(ending.format(offset))]
        except:
            date = [datetime.datetime.strptime(customdate[0], "%m/%d/%Y").strftime("%Y-%m-%d")+str(begninning.format(offset)),
                    datetime.datetime.strptime(customdate[0], "%m/%d/%Y").strftime("%Y-%m-%d")+str(ending.format(offset))]
    return date

def summaryPicker(date):
    if(date==""):
        summary = "Today's"
    elif (date=="today"):
        summary = "Today's"
    elif (date=="yesterday"):
        summary = "Yesterday's"
    elif (date=="week"):
        summary = "This Week's"
    elif (date=="month"):
        summary = "This Month's"
    elif (date=="year"):
        summary = "This Year's"
    elif (date=="lastweek"):
        summary = "Last Week's"
    elif (date=="lastmonth"):
        summary = "Last Month's"
    elif (date=="1stquarter"):
        summary = "1st Quarter's"
    elif (date=="2ndquarter"):
        summary = "2nd Quarter's"
    elif (date=="3rdquarter"):
        summary = "3rd Quarter's"
    elif (date=="4thquarter"):
        summary = "4th Quarter's"
    else:
        custom = date.split("-")
        #summary = "["+str(custom[0]) + " - " + str(custom[1]) + "] Custom"
        summary = "Custom"
    return summary

def thisDay(offset):
    date = offsetDate(offset)
    date0 = str(date) + begninning.format(offset)
    date1 = str(date) + ending.format(offset)
    return([date0,date1])

def yesterday(offset):
    today = offsetDate(offset)
    yesterday = today - datetime.timedelta(days=1)
    date0 = str(yesterday) + begninning.format(offset)
    date1 = str(yesterday) + ending.format(offset)
    return([date0,date1])

def thisMonth(offset):
    month1 = offsetDate(offset)
    month0 = month1.replace(day=1)
    return [str(month0)+str(begninning.format(offset)),
            str(month1)+str(ending.format(offset))]

def thisWeek(offset):
    week1 = offsetDate(offset)
    lastMonth = week1 - datetime.timedelta(days=7)
    week0 = lastMonth.strftime("%Y-%m-%d")
    return ([str(week0)+str(begninning.format(offset)),
             str(week1)+str(ending.format(offset))])

def thisYear(offset):
    year1 = offsetDate(offset)
    year0 = year1.replace(day=1,month=1)
    return([str(year0)+str(begninning.format(offset)),
            str(year1)+str(ending.format(offset))])

def lastWeek(offset):
    today = offsetDate(offset)
    lastWeek1 = today - datetime.timedelta(days=1)
    lastWeek0 = lastWeek1 - datetime.timedelta(days=7)
    print (lastWeek1)
    print (lastWeek0)
    return([str(lastWeek0)+str(begninning.format(offset)),
    str(lastWeek1)+str(ending.format(offset))])

def lastMonth(offset):
    today = offsetDate(offset)
    first = today.replace(day=1)
    lastMonth = first - datetime.timedelta(days=1)
    dateLastMonth1 = lastMonth.strftime("%Y-%m-%d")
    a = dateLastMonth1.split("-")
    dateLastMonth0 = a[0] + "-" + a[1] + "-" + "01"
    return([str(dateLastMonth0)+str(begninning.format(offset)),
    str(dateLastMonth1)+str(ending.format(offset))])

def firstQuarter(offset):
    now = offsetDate(offset)
    return([str(now.year)+"-01-01"+str(begninning.format(offset)),
    str(now.year)+"-03-31"+str(ending.format(offset))])

def secondQuarter(offset):
    now = offsetDate(offset)
    return([str(now.year)+"-04-01"+str(begninning.format(offset)),
    str(now.year)+"-06-30"+str(ending.format(offset))])

def thirdQuarter(offset):
    now = offsetDate(offset)
    return([str(now.year)+"-07-01"+str(begninning.format(offset)),
    str(now.year)+"-09-30"+str(ending.format(offset))])

def fourthQuarter(offset):
    now = offsetDate(offset)
    return([str(now.year)+"-10-01"+str(begninning.format(offset)),
            str(int(now.year)+1)+"-12-31"+str(ending.format(offset))])

def offsetDate(offset):
    flag = 1
    if(offset[0]=="-"):
        flag = -1
    hours = int(str(offset[1])+str(offset[2]))
    min = int(str(offset[3])+str(offset[4]))
    date_time = datetime.datetime.utcnow().replace(microsecond = 0)
    date_time = date_time + (datetime.timedelta(hours=hours, minutes=min)*flag)
    date = date_time.date()
    return date

#datetime.datetime(2012, 12, 26, 17, 18, 52, 167840)
